import pathlib
import re
import json
from pathlib import Path
import getpass
from cripto import *

class persona():
    def __init__(self):
        pass

    def registro(self):
        # Se piden todos los datos del usuario
        self.nombre = input ("Introduce tu nombre: \n")
        self.apellido = input("Introduce tu apellido: \n")
        self.fecha = input ("Introduce tu fecha de cumpleaños: \n")
        self.DNI = ""
        while self.validar_dni(self.DNI) != True:
            self.DNI = input ("Introduce tu DNI: \n")
        self.usuario = input("Introduce tu nombre de usuario: \n")
        self.contrasena = input("Introduce tu contraseña: \n")
        self.dinero = "1000"
        self.rol = "Usuario"
        # Se mete en un json los datos del usuario basicos
        json_users = str(pathlib.Path().absolute()) + "\json_users.json"
        data_list = self.abrir_json(json_users)

        dic_usuario = {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha": self.fecha,
            "DNI": self.DNI,
            "Rol": self.rol,
            "usuario": self.usuario
        }
        if len(data_list) == 0:
            generar_key()
        data_list.append(dic_usuario)

        clave = obtener_clave("usuario")
        self.actualizar_json(data_list , json_users)
        encriptar_registro(clave)

        # Se mete en otro json la contraseña del usuario
        json_contrasena = str(pathlib.Path().absolute()) + "\json_contrasenas.json"
        data_contrasenas = self.abrir_json(json_contrasena)
        dic_contrasena = {
            "usuario": self.usuario,
            "contrasena": (hashlib.sha256(self.contrasena.encode('utf-8')).hexdigest())
        }
        data_contrasenas.append(dic_contrasena)
        self.actualizar_json(data_contrasenas, json_contrasena)

        # Se mete en otro json el dinero del usuario
        json_dinero = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
        data_dinero = self.abrir_json(json_dinero)
        dic_dinero = {
            "usuario": self.usuario,
            "dinero": self.dinero,
        }
        if len(data_dinero) == 0:
            generar_key()
        clave = obtener_clave("dinero")
        data_dinero.append(dic_dinero)
        self.actualizar_json(data_dinero, json_dinero)
        encriptar_dinero(clave, self.usuario)

    def inicio_sesion(self):
        self.usuario = input("Introduce tu nombre de usuario\n")
        usuario_encontrado = self.validar_usuario()
        # Se busca al usuario introducido
        while usuario_encontrado == False: 
            print("Nombre de usuario incorrecto\n")
            isVolver = ""
            while isVolver != "1" and isVolver != "2":
                # Si se falla se pregunta si quiere volver a introducirlo o si quiere volver al menu
                isVolver = input("1: Volver a introducir el usuario\n"
                                 "2: Salir al menu de inicio\n")
            if isVolver == "1":
                # Si no existe el usuario se vuelve a preguntar el nombre
                self.usuario = input("Introduce tu nombre de usuario\n")
                usuario_encontrado = self.validar_usuario()
            else:
                return 0

        # Se comprueba que la contraseña sea correcta
        contrasena = input("Introduce tu contraseña: \n")
        contrasena = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
        if usuario_encontrado["contrasena"] != contrasena:
            print ("Contraseña incorrecta\n")
            return 0
        self.rol = self.buscar_usuario()["Rol"]
            
    def validar_dni(self, dni: str):
        # Funcion que valida el dni
        INVALIDOS = {"00000000T", "00000001R", "99999999R"}
        DIGITO_CONTROL = "TRWAGMYFPDXBNJZSQVHLCKE"
        REGEXP = "[0-9]{8}[A-Z]"
        return dni not in INVALIDOS \
        and re.match(REGEXP, dni) is not None \
        and dni[8] == DIGITO_CONTROL[int(dni[0:8]) % 23]

    def validar_usuario(self):
        # Funcion que comprueba que exista el usuario
        json_contrasena = str(pathlib.Path().absolute()) + "\json_contrasenas.json"
        data_list = self.abrir_json(json_contrasena)
        for user in data_list:
            if user["usuario"] == self.usuario:
                return user
        return False

    def obtener_dinero(self):
        # Funcion que comprueba que exista el usuario
        json_contrasena = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
        data_list = self.abrir_json(json_contrasena)
        clave = obtener_clave("dinero")
        return desencriptar_dinero(clave, self.usuario)

    def abrir_json(self, path):
        # Funcion que abre el json y devuelve la lista de elemetos del json
        try:
            with open(path, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)

        # Comprueba que se ha creado el archivo correctamente
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as e:
            raise "JSON Decode Error - Wrong JSON Format" from e
        return data_list

    def actualizar_json(self, data_list , path):
        # Actualiza el json con la nueva lista de elementos
        try:
            with open(path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as e:
                raise "Wrong file or file path" from e

    def retirar(self, dinero_retirado = 0):
        preguntar = 0
        if dinero_retirado == 0:
            preguntar = 1
        # Se abre el json donde está el dinero del usuario
        json_dinero = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
        # Se busca al usuario
        usuario = self.obtener_dinero()
        data_list = self.abrir_json(json_dinero)
        retirada_correcta = False
        # Se comprueba que el dinero que quiere retirar es correcto

        while retirada_correcta == False:
            if preguntar == 1:
                dinero_retirado = input ("¿Cuantas Watón Coins quiere retirar?\n")
            # Si tiene dinero sufuciente, se retirara el dinero de la cuenta
            if int(dinero_retirado) <= int(usuario["dinero"]):
                data_list.remove(usuario)
                usuario["dinero"] = str(int(usuario["dinero"]) - int(dinero_retirado))
                print ("Se han retirado:", dinero_retirado, "de tu cuenta.\nTu saldo restante es:",usuario["dinero"] , "Watón Coins\n")
                retirada_correcta = True
            else:
                # Si no tiene dinero suficiente vuelve a preguntar
                print("No tienes suficiente dinero, tu saldo es:", usuario["dinero"] , "Watón Coins\n")
        # Se actualiza el json
        clave = obtener_clave("dinero")
        data_list.append(usuario)
        self.actualizar_json(data_list, json_dinero)
        encriptar_dinero(clave, self.usuario)



    def ingresar(self, dinero_ingresado = 0):
        preguntar = 0
        if dinero_ingresado ==0:
            preguntar = 1
        # Se abre el json donde está el dinero del usuario
        json_dinero = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
        # Se busca al usuario
        usuario = self.obtener_dinero()
        data_list = self.abrir_json(json_dinero)
        ingreso_correcto = False
        # Se comprueba que el dinero que quiere ingresar es correcto
        while ingreso_correcto == False:
            if preguntar == 1:
                dinero_ingresado = input ("¿Cuantas Watón Coins quiere ingresar?\n")
            # Se comprueba que se ingresa un numero positivo
            if int(dinero_ingresado) > 0:
                data_list.remove(usuario)
                usuario["dinero"] = str(int(usuario["dinero"]) + int(dinero_ingresado))
                print ("Se han añadido:", dinero_ingresado, "a tu cuenta.\n Tu saldo actual es:",usuario["dinero"], "Watón Coins\n")
                ingreso_correcto = True
            else:
                print("No puedes ingresar Watón Coins negativas Watón\n")
        # Se actualiza el json
        clave = obtener_clave("dinero")
        data_list.append(usuario)
        self.actualizar_json(data_list, json_dinero)
        encriptar_dinero(clave, self.usuario)

    def imprimir_usuario(self):
        clave = obtener_clave("usuario")
        usuario_actual = desencriptar_usuario(clave, self.usuario)
        print ("Nombre: " + usuario_actual["nombre"]  + "\n")
        print ("Apellido: " + usuario_actual["apellido"]  + "\n")
        print ("Fecha: " + usuario_actual["fecha"]  + "\n")
        print ("DNI: " + usuario_actual["DNI"]  + "\n")
        print ("Usuario: " + self.usuario  + "\n")
        
    def buscar_usuario(self):
        # Funcion que comprueba que exista el usuario
        json_users = str(pathlib.Path().absolute()) + "\json_users.json"
        data_list = self.abrir_json(json_users)
        for user in data_list:
            if user["usuario"] == self.usuario:
                return user
        return False