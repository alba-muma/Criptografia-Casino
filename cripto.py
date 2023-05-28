import cryptography.fernet
from cryptography.fernet import Fernet
import hashlib
import pathlib
import re
import json
from pathlib import Path


from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def json_abierto(path):
    # Se abre el json
    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
    # Comprueba que se ha creado el archivo correctamente
    except json.JSONDecodeError as e:
        raise "JSON Decode Error - Wrong JSON Format" from e
    return data_list

def encriptar_registro (clave):
    # Obtiene la ruta del archivo json_users
    path = str(pathlib.Path().absolute()) + "\json_users.json"
    # Codifica la clave a bytes para utilizar fernet
    clave = clave.encode('utf-8')
    fernet = Fernet(clave)
    # Se abre el json
    data_list = json_abierto(path)
    n = len(data_list) - 1 # Usuario del que se está haciendo el registro
    # Encripta los datos y los guarda en la lista que se guardará en el JSON
    data_list[n]["nombre"] = (fernet.encrypt(data_list[n]["nombre"].encode('utf-8'))).decode('utf-8')
    data_list[n]["apellido"] = (fernet.encrypt(data_list[n]["apellido"].encode('utf-8'))).decode('utf-8')
    data_list[n]["fecha"] = (fernet.encrypt(data_list[n]["fecha"].encode('utf-8'))).decode('utf-8')
    data_list[n]["DNI"] = (fernet.encrypt(data_list[n]["DNI"].encode('utf-8'))).decode('utf-8')
    # Abre el JSON y guarda la lista con los datos encriptados
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)
    except FileNotFoundError as e:
            raise "Wrong file or file path" from e

def encriptar_dinero(clave, user):
    # Obtiene la ruta del archivo json_watonCoins
    path = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
    # Codifica la clave a bytes para utilizar fernet
    clave = clave.encode('utf-8')
    fernet = Fernet(clave)
    # Se abre el json
    data_list = json_abierto(path)
    for n in range(len(data_list)):
        # Busca al usuario del cual se va a encriptar su dinero
        if data_list[n]["usuario"] == user:
            # Encripta el dinero del usuario y lo guarda en en la lista que se guardará en el JSON
            data_list[n]["dinero"] = (fernet.encrypt(data_list[n]["dinero"].encode('utf-8'))).decode('utf-8')
    #Abre el JSON y guarda la lista con los datos encriptados
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)
    except FileNotFoundError as e:
            raise "Wrong file or file path" from e

def desencriptar_dinero(clave, user):
    # Obtiene la ruta del archivo json_watonCoins
    path = str(pathlib.Path().absolute()) + "\json_watonCoins.json"
    # Codifica la clave a bytes para utilizar fernet
    clave = clave.encode('utf-8')
    fernet = Fernet(clave)
    # Se abre el json
    data_list = json_abierto(path)
    for n in range(len(data_list)):
        # Busca al usuario del cual se va a desencriptar su dinero
        if data_list[n]["usuario"] == user:
            # Desencripta el dinero del usuario y lo guarda en en la lista que se guardará en el JSON
            data_list[n]["dinero"] = (fernet.decrypt(data_list[n]["dinero"].encode('utf-8'))).decode('utf-8')
            usuario_actual = data_list[n]
    # Abre el JSON y guarda la lista con los datos desencriptados
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)
    except FileNotFoundError as e:
        raise "Wrong file or file path" from e
    return usuario_actual

def desencriptar_usuario (clave, user):
    # Obtiene la ruta del archivo json_users
    path = str(pathlib.Path().absolute()) + "\json_users.json"
    # Codifica la clave a bytes para utilizar fernet
    clave = clave.encode('utf-8')
    fernet = Fernet(clave)
    # Se abre el json
    data_list = json_abierto(path)
    for item in data_list:
        # Busca al usuario del cual se van a desencriptar sus datos
        if item["usuario"] == user:
            usuario_actual = item
    # Desencripta los datos y los guarda en la lista que se guardará en el JSON
    usuario_actual["nombre"] = (fernet.decrypt(usuario_actual["nombre"].encode('utf-8'))).decode('utf-8')
    usuario_actual["apellido"] = (fernet.decrypt(usuario_actual["apellido"].encode('utf-8'))).decode('utf-8')
    usuario_actual["fecha"] = (fernet.decrypt(usuario_actual["fecha"].encode('utf-8'))).decode('utf-8')
    usuario_actual["DNI"] = (fernet.decrypt(usuario_actual["DNI"].encode('utf-8'))).decode('utf-8')
    return usuario_actual

def obtener_clave (tipo):
    path = "E:\json_key.json"
    # Se abre el json
    datos = json_abierto(path)
    #Devuelve la clave que encripta los datos que se pidan, es decir, los datos del usuario o su dinero
    if tipo == "usuario":
        return datos[0]["clave"]
    elif tipo == "dinero":
        return datos[1]["clave"]
    else:
        return -1

def generar_key ():
    # Obtiene la ruta del archivo json_key
    path = "E:\json_key.json"
    # Genera una clave que se va a guardar en el archivo JSON
    key = Fernet.generate_key()
    # Abre y lee el archivo donde se va a guardar la nueva clave
    try:
        with open(path, "r", encoding="utf-8", newline="") as file:
            data_list = json.load(file)
    except FileNotFoundError:
        data_list = []
    except json.JSONDecodeError as e:
        raise "JSON Decode Error - Wrong JSON Format" from e

    # Crea un diccionario con la clave nueva y lo añade a data_list
    dic_claves = {
        #Decodifica la clave para guardarla como string
        "clave": key.decode('utf-8')
    }
    data_list.append(dic_claves)
    #Abre el archivo y guarda la nueva clave
    try:
        with open(path, "w", encoding="utf-8", newline="") as file:
            json.dump(data_list, file, indent=2)
    except FileNotFoundError as e:
            raise "Wrong file or file path" from e

def firmar():
    print("Preparando su comunicado mensual...\n")

    # Se obtiene el mensaje
    mensaje = obtener_mensaje()
    print ("El comunicado es:")
    # Imprimimos el mensaje por pantalla para la simulación
    print (mensaje)
    # Pasamos el mensaje a bytes
    mensaje = mensaje.encode("utf-8")
    # Obtenemos la clave privada de A
    clave_privada = open("./PRACTICA/A/Akey.pem" , "rb").read()
    # Se introduce la passpharase para obtener la clave
    clave = RSA.import_key(clave_privada, passphrase = "pepelaranaA")
    # Obtenemos el resumen del mensaje
    resumen = SHA256.new(mensaje)
    # Se firma el mensaje
    firma = pkcs1_15.new(clave).sign(resumen)

    print ("Firmando...")
    return firma

def validar_firma(firma):
    # Se obtiene el mensaje y se pasa a bytes
    mensaje = obtener_mensaje().encode("utf-8")

    # Se abre el documento donde esta la clave publica de a
    clave_publica = RSA.import_key(open("./PRACTICA/A/Acert.pem").read())
    # Se genera el resumen del mensaje
    resumen = SHA256.new(mensaje)
    print ("Validando firma...")
    try:
        # Se comprueba que la firma es correcta
        pkcs1_15.new(clave_publica).verify(resumen, firma)
        print("La firma es válida")
    except (ValueError, TypeError):
        #Si no es correcta
        print ("La firma no es válida \n")

def obtener_mensaje ():
    # Se abre el json donde está el comunicado del director
    path = str(pathlib.Path().absolute()) + "\json_mensaje.json"
    # Se extrae el diccionario donde está el mesnaje
    dic = json_abierto(path)
    # Se extrae el mensaje del diccionario
    mensaje = dic["mensaje"]
    return mensaje

