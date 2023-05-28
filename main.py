import json
import random
from persona import persona
from cripto import *

class casino:
    def __init__(self):
        pass

    def menu_inicio(self):
        opcion = 0
        print("¡Bienvenido a Casino Watón!\n")
        # Menu de registro e inicio sesion
        while opcion != "1" and opcion != "2" and opcion != "3":
            opcion = input("Seleccione una opción:\n"
                       "1:Iniciar sesión\n"
                       "2:Registrarse\n"
                       "3:Salir\n")

            if opcion != "1" and opcion != "2" and opcion != "3":
                print("Error, seleccione una opción válida")
        # Opcion de inicio sesion
        if opcion == "1":
            usuario = persona()
            a = usuario.inicio_sesion()
            # Si al final no quiere iniciar sesion
            if a == 0:
                self.menu_inicio()
            else: 
                # Redirigimos al usuario al menu del casino
                self.menu_principal(usuario)
        # Opcion de registro
        elif opcion == "2":
            usuario = persona()
            # Registro
            usuario.registro()
            # Redirigimos al usuario al menu del casino
            self.menu_principal(usuario)
        # Salir de la aplicacion
        else:
            print("¡Muchas gracias Waton/a!")
            return 0

    def menu_principal(self, nombre):
        print("Bienvenido,", nombre.usuario)
        operacion = ""
        # Menu de opciones dentro del casino
        if nombre.rol == "Admin":
            opciones = ["1", "2", "3", "4", "5", "6", "7"]
        else:
            opciones = ["1", "2", "3", "4", "5", "6"]
        while(operacion not in opciones):
            print ("¿Que quieres hacer hoy," , nombre.usuario,"?\n")
            print ("1:Ruleta\n"
                              "2:BlackJack\n"
                              "3:Ingresar dinero\n"
                              "4:Retirar dinero\n"
                              "5:Consultar datos personales\n"
                              "6:Cerrar sesión")
            if nombre.rol == "Admin":
                print ("7: Enviar comunicado")
            operacion = input ("Introduce la operación: \n")
            if (operacion not in opciones):
                print("Operación inválida")
        # Jugar a la ruleta
        if operacion =="1":
            self.ruleta(nombre)
            self.menu_principal(nombre)
        # Jugar al blackjack
        elif operacion =="2":
            self.blackjack(nombre)
            self.menu_principal(nombre)
        # Ingresar dinero
        elif operacion =="3":
            nombre.ingresar()
            self.menu_principal(nombre)
        # Retirar dinero
        elif operacion =="4":
            nombre.retirar()
            self.menu_principal(nombre)
        elif operacion =="5":
            nombre.imprimir_usuario()
            self.menu_principal(nombre)
        elif operacion == "7":
            firma = firmar()
            validar_firma(firma)
            self.menu_principal(nombre)
        else:
            # Cerrar sesion
            print("¡Vuelva pronto Watón!", nombre.usuario)
            self.menu_inicio()

    def ruleta(self, usuario):
        dineros = ""
        dinero_correcto = False
        usuario_dinero = usuario.obtener_dinero()
        # Se pregunta al usuario que cantidad de dinero quiere apostar
        while dinero_correcto == False:
            dineros = input("¿Cuanto dinero quiere apostar?\n")
            # Se comprueba que se haya introducido un numero mayor a 0
            if dineros == "0" or dineros.isdigit() == False:
                # Echamos al usuario del casino por vacilar
                print("En Casino Watón tenemos una politica de juego seria, por aquí no vuelva\n")
                return 0
            # Se comprueba que el usuario tenga dinero suficiente
            elif int(dineros) <= int(usuario_dinero["dinero"]):
                dinero_correcto = True
            else:
                print("No tienes dinero suficiente, tu saldo es de:", usuario_dinero["dinero"] , "\n")
        clave = obtener_clave("dinero")
        encriptar_dinero(clave, usuario.usuario)
        apuesta = 38
        # Se pregunta a que numero quiere apostar
        while int(apuesta) not in range(37):
            apuesta = input("¿A que número desea apostar? (Número entre 0 y 36)\n")

        # Se activa la ruleta y la bola acabara en un numero de 1 al 36
        resultado = random.randint(0, 36)
        print ("¡Ha salido el número:" , resultado , "!\n")
        # Si el resultado es 0 y el usuario ha acerdado se multiplica su apuesto x13
        if resultado == 0 and int(apuesta) == 0:
            dineros = int(dineros) * 13
            usuario.ingresar(dineros)
        # Si el usuario ha apostado por un numero impar y sale un impar se ingresa su apuesta (igual para par-par)
        elif (resultado % 2 == int(apuesta) % 2 and int(apuesta) != 0):
            usuario.ingresar(dineros)
        else:
        # Si no, el usuario pierde su apuesta
            print("¡Mala suerte, has perdido!")
            usuario.retirar(dineros)

    def blackjack(self, usuario):
        dinero = ""
        dinero_correcto = False
        # Se pregunta al usuario que cantidad de dinero quiere apostar
        usuario_dinero = usuario.obtener_dinero()
        while dinero_correcto == False: 
            dinero = input("¿Cuanto dinero quiere apostar?\n")
            # Se comprueba que se haya introducido un numero mayor a 0
            if dinero == "0" or dinero.isdigit() == False:
                # Echamos al usuario del casino por vacilón
                print("En Casino Watón tenemos una politica de juego seria, por aquí no vuelva\n")
                return 0
            # Se comprueba que el usuario tenga dinero suficiente
            elif int(dinero) <= int(usuario_dinero["dinero"]):
                dinero_correcto = True
            else:
                print("No tienes dinero suficiente, tu saldo es de:", usuario_dinero["dinero"] , "\n")
        clave = obtener_clave("dinero")
        encriptar_dinero(clave, usuario.usuario)

        # Generamos la baraja de cartas
        valores = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
        palos = ['DIAMANTES', 'TREBOLES', 'PICAS', 'CORAZONES']
        cartas = []
        for palo in palos:
            for valor in valores:
                cartas.append([valor , palo])

        # Se desordena la lista, para simular que se ha barajeado
        print("Barajeando...")
        random.shuffle(cartas)

        # Variables para el conteo de puntos y para saber que cartas tiene cada usuario
        cartas_casa = []
        cartas_jugador = []
        puntuacion_casa = 0
        puntuacion_jugador = 0

        # Se empieza sabiendo una carta de la mesa
        cartas_casa.append(cartas.pop())
        puntuacion_casa += self.valor_carta(cartas_casa[-1])

        # Se empieza con dos cartas en mano
        cartas_jugador.append(cartas.pop())
        puntuacion_jugador += self.valor_carta(cartas_jugador[-1])
        cartas_jugador.append(cartas.pop())
        puntuacion_jugador += self.valor_carta(cartas_jugador[-1])

        # Imprimimos las cartas y puntuacion del principio de ronda
        print ("Tus cartas son:",cartas_jugador ,"\n")
        print("El valor de tus cartas son:", puntuacion_jugador, "\n")
        print ("Las cartas de la casa son:", cartas_casa ,"\n")
        print("El valor de las cartas de la casa son:", puntuacion_casa, "\n\n")

        # Se le pregunta al usuario si quiere pedir otra carta, hasta que diga que no o supere los 21 puntos
        decision_carta = ""
        while decision_carta.upper() != "N" and puntuacion_jugador < 21:
            decision_carta = input ("¿Pides otra carta? S/N")
            if decision_carta.upper() == "S":
                cartas_jugador.append(cartas.pop())
                puntuacion_jugador += self.valor_carta(cartas_jugador[-1])
                print("Tus cartas son:", cartas_jugador, "\n")
                print("El valor de tus cartas son:", puntuacion_jugador, "\n")
                print("Las cartas de la casa son:", cartas_casa, "\n")
                print("El valor de las cartas de la casa son:", puntuacion_casa, "\n\n")

        # Si el jugador supera los 21 puntos ha perdido
        if puntuacion_jugador > 21:
            print ("!Perdiste Watón! Otra vez será.")
            usuario.retirar(dinero)

        else:
            # Una vez ha terminado el jugador, la casa pide mas cartas hasta que supere al jugador o se pase de 21 puntos
            while puntuacion_jugador >= puntuacion_casa:
                cartas_casa.append(cartas.pop())
                puntuacion_casa += self.valor_carta(cartas_casa[-1])
                print("Tus cartas son:", cartas_jugador, "\n")
                print("El valor de tus cartas son:", puntuacion_jugador, "\n")
                print("Las cartas de la casa son:", cartas_casa, "\n")
                print("El valor de las cartas de la casa son:", puntuacion_casa, "\n\n")
            # Si la puntuacion de ambos es igual, habrá un empate y se le devuelve la apuesta al jugador
            if puntuacion_casa == puntuacion_jugador:
                print("!Empate Watón! Ni pierdes ni ganas tu apuesta.")
            # Si la casa tiene mas de 21 puntos, gana el jugador y se le ingresa lo apostado
            elif puntuacion_casa > 21:
                print("La casa pierde, puntuacion de la casa: " , puntuacion_casa , "\n")
                usuario.ingresar(dinero)
            # En todas las demas opciones la casa tiene mas puntos que el jugador y pierde el jugador
            # El jugador pierde lo apostado
            else:
                print("!Perdiste Watón! Otra vez será.")
                usuario.retirar(dinero)

    # Funcion que devuelve el valor de cada carta
    def valor_carta(self, carta):
        # El "A" vale 1
        if carta[0] == "A":
            valor = 1
        # Las figuras valen 10
        elif carta[0] == "J" or carta[0] == "Q" or carta[0] == "K":
            valor = 10
        # El resto de cartas valen su numero
        else:
            valor = carta[0]
        return valor



# Se crea el casino
hola = casino()

# Se inica el casino
hola.menu_inicio()




