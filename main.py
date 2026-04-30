import random
import pygame
import os
import time
import pyfiglet
import tabulate
import csv
os.system('cls')
#Librerias a instalar. pygame, pyfiglet, tabulate

#Inicializamos pygame
pygame.init()
pygame.mixer.init()

#VARIABLES DEL ALGORITO GENERAL
datoPuntos = [] #lista que sera usada como tabla para los puntos
puntosNumRandom = 0 #variable sumadora para el juego numero random
puntosPPT = 0 #variable sumadora para el juego piedra papel o tijera
puntosPyR = 0 #variable sumadora para el juego preguntas y respuestas
puntosAhorcado = 0 #variable sumadora para el juego ahorcado
puntosTotales = 0 #Variable para calcular los puntos totales

#FUNCIONES PYGAME
def controlar_musica(): #Funcion para controlar la musica
    pygame.mixer.music.load("Alpha2CSTheme.mp3") #Selecciona el archivo de musica
    pygame.mixer.music.play(loops=-1) #Coloca que se quede en un loop
    pygame.mixer.music.set_volume(0.05) #Pone el volumen bajo
    
def controlar_sonidos(): #Funcion para controlar sonidos
    sonido = pygame.mixer.Sound("sfx_insertcredit.wav") #Selecciona el sonido
    sonido.set_volume(0.20) #Le da el valor de volumen
    sonido.play() #Lo comienza
    
def eleccion_correcta():
    sonido = pygame.mixer.Sound("Choice-Right.wav") #Selecciona el sonido
    sonido.set_volume(0.35) #Le da el valor de volumen
    sonido.play() #Lo comienza

def eleccion_incorrecta():
    sonido = pygame.mixer.Sound("Choice-Wrong.wav") #Selecciona el sonido
    sonido.set_volume(0.35) #Le da el valor de volumen
    sonido.play() #Lo comienza
    
def GameOver():
    sonido = pygame.mixer.Sound("Gameover.wav") #Selecciona el sonido
    sonido.set_volume(0.35) #Le da el valor de volumen
    sonido.play() #Lo comienza

def GraciasPorJugar():
    sonido = pygame.mixer.Sound("Thanks.wav") #Selecciona el sonido
    sonido.set_volume(0.35) #Le da el valor de volumen
    sonido.play() #Lo comienza

#FUNCIONES GENERALES        
def crearTabladeJuego(usuario,puntos,juego): #Funcion para tablas de puntaje en los juegos
    nombre_archivo = juego #definimos el nombre del archivo, en ese caso se pasa como argumento desde el juego
    encabezados = ['usuario', 'puntos'] #definimos encabezados
    datos_actualizados = [] #lista donde se guardan los datos actualizados
    usuario_encontrado = False #bool para ver si encontramos al usuario
    if os.path.exists(nombre_archivo): #verifica si el archivo existe 
        try: #comenzamos con manejo de excepciones
            with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv_lectura: #abrimos el archivo
                lector_csv = csv.DictReader(archivo_csv_lectura) #lo leemos
                for fila in lector_csv: #contador que cuenta cada fila en el archivo csv
                    fila['puntos'] = int(fila['puntos']) #convertimos el string de puntos a entero
                    datos_actualizados.append(fila) #guardamos la fila en la lista datos actualizados
        except IOError as e: 
            print(f"Error al leer el archivo '{nombre_archivo}': {e}") #si hay un error de I/O lanza un mensaje de error
            return #Salir de la función si hay error de lectura
        except ValueError as e: 
            print(f"Error al convertir puntos a número en el archivo '{nombre_archivo}': {e}. Verifique el formato.") #error de formato
            return
    for fila in datos_actualizados: #contador de filas en la lista de datos actualizados
        if fila['usuario'] == usuario: #si se encuentra el usuario actual en la lista de datos
            fila['puntos'] += puntos #suma un punto dependiendo del juego
            usuario_encontrado = True #cambiamos el bool a true
            print(f"Puntaje de '{usuario}' actualizado. Nuevo total: {fila['puntos']}") #mensaje de confirmacion
            break

    if not usuario_encontrado: #si no se encuentra al usuario
        nueva_entrada = {'usuario': usuario, 'puntos': puntos} #lo crea como una nueva fila
        datos_actualizados.append(nueva_entrada) #guarda esa fila en los datos actualizados
        print(f"Nuevo usuario '{usuario}' agregado con {puntos} puntos.") #mensaje de confirmacion

    try: #manejo de excepciones al escribir en el archivo
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv_escritura: #abrimos el archivo
            escritor_csv = csv.DictWriter(archivo_csv_escritura, fieldnames=encabezados) #Le damos los parametros en como va a escribir
            escritor_csv.writeheader() 
            escritor_csv.writerows(datos_actualizados) #le escribe los datos de la lista datos actualizados
 
        print(f"Archivo '{nombre_archivo}' guardado exitosamente.") #mensaje de confirmacion

    except IOError as e: #excepcion para errores I/O
        print(f"Error al escribir en el archivo '{nombre_archivo}': {e}")

def mostrarTabla(datos): #muestra las tablas dependiendo de los datos que se envie como argumento
    print(tabulate.tabulate(datos,headers="keys", tablefmt="grid"))

def mostrarTablaPuntuacion(): #muestra la tabla de puntuacion general de todos los juegos
    nombre_archivo = "tablaPuntuacion.csv" #le damos el nombre del archivo
    datos_a_mostrar = [] #lista para mostrar datos

    if not os.path.exists(nombre_archivo) or os.stat(nombre_archivo).st_size == 0: #Si el archivo no existe o esta vacio devuelve un mensaje de error
        print(f"El archivo '{nombre_archivo}' no existe o está vacío. No hay datos para mostrar.")
        return

    try: #manejo de excepciones
        with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv: #abrimos el archivo
            lector_csv = csv.DictReader(archivo_csv) #leemos el archivo
            for fila in lector_csv: #por cada fila en el lecto
                try: #intenta convertir el dato puntos totales en un entero
                    fila['PuntosTotales'] = int(fila.get('PuntosTotales', 0))
                except ValueError: #si da error
                    fila['PuntosTotales'] = 0 #lo iguala a 0
                datos_a_mostrar.append(fila) #se coloca en la lista de datos a mostrar

        datos_ordenados = sorted(datos_a_mostrar, key=lambda x: x['PuntosTotales'], reverse=True) #ordena la lista por mayores puntos
        if datos_ordenados: #si los dato se ordenan
            headers = datos_ordenados[0].keys() # Usa las claves del diccionario como encabezados
            table_data = [list(d.values()) for d in datos_ordenados] 
            
            print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid")) # se imprimen con la libreria tabulate
        else:
            print("No hay datos válidos para mostrar.") #Si no hay datos validos para mostrar

    except IOError as e: #por si hay errores
        print(f"Error al leer el archivo '{nombre_archivo}': {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al mostrar la tabla: {e}")
 
def crearTablaDePuntuacion(usuario, puntosNumRandom, puntosPPT, puntosPyR, puntosAhorcado): #funcion para crear la tabla de puntuacion general
    nombre_archivo = "tablaPuntuacion.csv" #damos el nombre del archivo
    encabezados = ['Usuario', 'PuntosNumRandom', 'PuntosPPT', 'PuntosPyR', 'PuntosAhorcado','PuntosTotales'] #le damos los encabezados
    datos_actualizados = [] #lista para guardar los datos actualizados
    usuario_encontrado = False #bool para ver si encontramos al usuario

    if os.path.exists(nombre_archivo) and os.stat(nombre_archivo).st_size > 0: #si se encuentra el archivo
        try: #manejo de excepciones
            with open(nombre_archivo, 'r', newline='', encoding='utf-8') as archivo_csv_lectura: #abrimos el archivo en modo lectura
                lector_csv = csv.DictReader(archivo_csv_lectura) #leemos el archivo
                for fila in lector_csv:
                    try:  #recibe los datos del juego Adivinanza de numeros
                        puntos_num_random_existente = int(fila.get('PuntosNumRandom', 0))
                    except ValueError:
                        puntos_num_random_existente = 0
                    
                    try:  #recibe los datos del juego Piedra papel o tijera
                        puntos_ppt_existente = int(fila.get('PuntosPPT', 0))
                    except ValueError:
                        puntos_ppt_existente = 0

                    try:  #recibe los datos del juego trivia
                        puntos_PyR_existente = int(fila.get('PuntosPyR', 0))
                    except ValueError:
                        puntos_PyR_existente = 0
                    
                    try:  #recibe los datos del juego Adivinanza de numeros
                        puntos_ahorcado_existente = int(fila.get('PuntosAhorcado', 0))
                    except ValueError:
                        puntos_ahorcado_existente = 0

                    if fila['Usuario'] == usuario: #si se encuentra el usuario se suman sus puntos
                        fila['PuntosNumRandom'] = puntos_num_random_existente + puntosNumRandom
                        fila['PuntosPPT'] = puntos_ppt_existente + puntosPPT
                        fila['PuntosPyR'] = puntos_PyR_existente + puntosPyR
                        fila['PuntosAhorcado'] = puntos_ahorcado_existente + puntosAhorcado
                        
                        #calcula los puntos totales
                        fila['PuntosTotales'] = int(fila['PuntosNumRandom']) + \
                                                int(fila['PuntosPPT']) + \
                                                int(fila['PuntosPyR']) + \
                                                int(fila['PuntosAhorcado'])
                        
                        usuario_encontrado = True #encuentra el usuario
                        print(f"Puntajes de '{usuario}' actualizados.") #mensaje de confirmacion
                    
                    datos_actualizados.append(fila) #agrega los datos ya sean o no actualizados a la lista
        except IOError as e:
            print(f"Error al leer el archivo '{nombre_archivo}': {e}")
            return 

    #si el usuario no existe se crea como una nueva fila
    if not usuario_encontrado:
        puntos_totales = puntosNumRandom + puntosPPT + puntosPyR + puntosAhorcado
        nueva_fila = {
            'Usuario': usuario,
            'PuntosNumRandom': puntosNumRandom,
            'PuntosPPT': puntosPPT,
            'PuntosPyR': puntosPyR,
            'PuntosAhorcado': puntosAhorcado,
            'PuntosTotales': puntos_totales
        }
        datos_actualizados.append(nueva_fila) #se guarda en la lista
        print(f"Usuario '{usuario}' añadido con sus puntajes iniciales.") #mensaje de confirmacion

    try: #intenta sobreescribir los datos que ya estan en el archivo csv
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv_escritura: 
            escritor_csv = csv.DictWriter(archivo_csv_escritura, fieldnames=encabezados)
            escritor_csv.writeheader() #escribimos el encabezado
            escritor_csv.writerows(datos_actualizados)
        print(f"Archivo '{nombre_archivo}' guardado exitosamente.") #mensaje de confirmacion
    except IOError as e:
        print(f"Error al escribir el archivo '{nombre_archivo}': {e}") #mensaje de error

def verificarUsuario(archivocsv, usuario):
    try:
        with open(archivocsv, mode="r", newline="", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                if fila and fila[0] == usuario:
                    return True
        return False
    except FileNotFoundError:
        print(f"ERROR: El archivo {archivocsv} no existe!!")
        return False

#FUNCIONES ADIVINANZA DE NUMERO
def pedir_numero(intentos_realizados):
    while True:
        try:
            numero = int(input(f"Intento #{intentos_realizados + 1}: "))
            if 1 <= numero <= 10:
                return numero
            else:
                eleccion_incorrecta()
                print("El número debe estar entre 1 y 10.")
        except ValueError:
            eleccion_incorrecta()
            print("Por favor, ingrese un número válido.")

# Función que juega una ronda
def jugar_ronda(ronda_numero):
    numero_a_adivinar = random.randint(1, 10)
    numero_intentos = 0
    max_intentos = 5

    print(f"\nRonda {ronda_numero}: Tienes 5 intentos por cada ronda.")
    print("¡BUENA SUERTE!")

    while numero_intentos < max_intentos:
        numero_usuario = pedir_numero(numero_intentos)
        numero_intentos += 1

        if numero_usuario == numero_a_adivinar:
            eleccion_correcta()
            print(f"¡Increíble! Has adivinado el número en {numero_intentos} intento(s).")
            return True
        elif numero_usuario > numero_a_adivinar:
            eleccion_incorrecta()
            print("El número ingresado está por encima del número a adivinar.")
        else:
            eleccion_incorrecta()
            print("El número ingresado está por debajo del número a adivinar.")

    GameOver()
    print(f"\nLo siento, no has adivinado el número.")
    print(f"El número correcto era {numero_a_adivinar}.")
    print("RONDA FINALIZADA.")
    return False

# Función para manejar las partidas completas
def partidas():
    numero_rondas = 5
    rondas_ganadas = 0

    for ronda in range(1, numero_rondas + 1):
        gano = jugar_ronda(ronda)
        if gano:
            global puntosNumRandom
            puntosNumRandom +=1
            rondas_ganadas += 1

    print(f"\nEl juego ha terminado. Ganaste {rondas_ganadas} de {numero_rondas} rondas.")

# Menú principal
def menu_principal():
    while True:
        partidas()
        jugar_nuevamente = input("\n¿Quieres jugar otra vez? (s/n): ").lower()
        if jugar_nuevamente != 's':
            print("¡Gracias por jugar! Hasta pronto.")
            break


#FUNCIONES PIEDRA PAPEL TIJERA

def traducir(opcion):
    return {1: "Piedra", 2: "Papel", 3: "Tijera"}.get(opcion, "Desconocido")

#FUNCIONES TRIVIA
def jugar_nivel(preguntas, opciones, respuestas): #en esta funcion se definen los parametros que usaremos para este caso usaremos las listas preguntas, opciones, respuestas.
    predicciones = {} #diccionario de predicciones lo usaremos para guardar las respuestas de los usuarios
    puntaje = 0 #contador de puntos se inicia en cero

    #bucle for para preguntas
    for i in range(len(preguntas)): #len nos ayuda a recorrer todas las preguntas usando su indice, i se utiliza para recorrer el indice recordando que los indices es la poscicion 0 1 2 
        print("\n-----------------------")
        print(preguntas[i]) #muestra la pregunta actual
        for opcion in opciones[i]: #este bucle dentro del bucle principal recorre las opciones correspondientes a la pregunta actual
            print(opcion) #muestra las opciones que asignamos en la lista A B C D

        while True: #En este bucle es para validacion de los datos que el usuario ingrese sean correctos
            respuesta_usuario = input("Tu respuesta (A, B, C o D): ").upper() #Pide la respuesta del usuario y el .upper lo convierte a mayuscula aunque el usuario lo escriba en minucula
            if respuesta_usuario == "SALIR": #si el usuario decide salir este if nos permitira salir del bucle While
                print("Has decidido salir del juego....")
                break
            elif respuesta_usuario in ["A", "B", "C", "D"]: #En este if verficamos si la respuesta es valida
                predicciones[preguntas[i]] = respuesta_usuario #esta variable guarda la respuestas del usuario para el diccionario de predicciones
                if respuesta_usuario == respuestas[i]: #este if nos ayudara a verificar si la respuesta es valida. recordemos que estamos en [i] es decir en el indice de esa respuesta
                    eleccion_correcta()
                    print("¡Correcto!") #mensaje de correcto si la respuesta es correcta 
                    puntaje += 1 #y si es correcto se usa el +=1 para sumar un punto al contador que inicio en cero
                    global puntosPyR
                    puntosPyR +=1
                else: #usamos else por que no haremos mas verificacion que solo correcto o incorrecto
                    eleccion_incorrecta()
                    print(f"Incorrecto. La respuesta correcta es: {respuestas[i]}") #le muestra al usuario mensaje de respuesta incorrecta le muestra la respuesta correcta llamando a [i] la respuesta correcta de esa pregunta
                break  # Salimos del bucle while para poder pasar a la siguiente pregunta
            else: #este else es para validar que solo se ingresen las opciones que pedimos en este caso A B C o D si el usuario ingresara Z ...
                print("ERROR: Debes ingresar solo A, B, C o D.") #le mostrara este mensaje que le indique que solo puede ingresar las opcines validas
                # No usamos break aquí, para que vuelva a preguntar
        if respuesta_usuario== "SALIR":
            break #con este salimos del bucle for para que no siga con mas preguntas si el usuario decidio salir

    print("\nRESULTADOS DEL NIVEL")
    print("-"*115)
    for i in range(len(preguntas)): #recorremos nuevamente las preguntas para mostrar las respuestas
        pregunta = preguntas[i] #Guarda la pregunta actual
        if pregunta in predicciones: #este if es por la opcion salir si el usuario no repondio ciertas preguntas no se mostraran todas solo las que respondio
            correcta = respuestas[i] #cguarda la respuesta correcta
            usuario = predicciones[pregunta] #almacena la respuesta del usuario
            resultado = "Correcta" if usuario == correcta else f"Incorrecta (Correcta: {correcta})" #Valida si la respuesta del usuario fue correcta o no
            print(f"{pregunta} Tu respuesta: {usuario} - {resultado}") #Imprime el resumen de la pregunta

    print(f"\nPuntaje en este nivel: {puntaje}/{len(predicciones)}") #imprime el puntaje obtenido del total de respuestas correctas o las que el usuario respondio
#fin de funcion de jugar nivel

def nivel_facil():
    preguntas = (
        "¿Cuál es el lugar más frío de la Tierra?: ",
        "¿Cuál es el río más largo del mundo?: ",
        "¿Dónde se originaron los juegos olímpicos?: ",
        "¿Cuál es el océano más grande?: ",
        "¿Cuál es el tercer planeta del sistema solar?: "
    )
    opciones = (
        ("A. Rusia", "B. La Antártida", "C. Alaska", "D. Polo Norte"),
        ("A. Amazonas", "B. Nilo", "C. Lempa", "D. Misisipi"),
        ("A. Estados Unidos", "B. Brasil", "C. Grecia", "D. Olimpia"),
        ("A. Atlántico", "B. Pacífico", "C. Índico", "D. Mar Muerto"),
        ("A. Planeta Tierra", "B. Marte", "C. Saturno", "D. Urano")
    )
    respuestas = ("B", "A", "C", "B", "A")
    jugar_nivel(preguntas, opciones, respuestas)
    
def nivel_medio():
    preguntas = (
        "¿Que pais fue el primero en emitir una moneda?: ",
        "¿Cuando acabo la segunda guerra mundial?: ",
        "Segun la biblia ¿Cuantos años vivio Matusalen?: ",
        "¿Cual fue la primera civilizacion humana?: ",
        "¿Que personaje fue conocido como el rey de Macedonia?: ",
        "Segun la leyenda ¿Quienes fundaron Roma?: ",
        "¿Quien fundo el socialismo cientifico?: ",
        "¿Quien es conocida como la primera programadora de computadoras?: ",
        "¿Que civilizacion antigua otorgo a las mujeres los mismos derechos al trono?: ",
        "¿Cual es la ciudad de los rascacielos?: ",
    )
    opciones = (
    ("A. El Salvador", "B. Estados Unidos", "C. Lidia", "D. Inglaterra"),
    ("A. 2000", "B. 1914", "C. 1938", "D. 1945"),
    ("A. 120", "B. 969", "C. 400", "D. 85"),
    ("A. Sumeria", "B. Egipcia", "C. Vikingos", "D. Eslavos"),
    ("A. Ramses", "B. David", "C. Alejadnro Magno", "D. Luis XIV"),
    ("A. Cesar y Augusto", "B. Romulo y Remo", "C. Neron", "D. Tito Tacio"),
    ("A. Vladimir Lenin", "B. Fidel Castro", "C. Newton", "D. Karl Marx"),
    ("A. Ada Lovelace", "B. Edith Clarke", "C. Selena Quintanilla", "D. Princesa Diana"),
    ("A. Civilizacion Griega", "B. Civilizacion Egipcia", "C. Civilacion India", "D. Civilizacion Salvadoreña"),
    ("A. Antigua Guatemala", "B. Hong Kong", "C. Nueva York", "D. Milan"),
    )
    respuestas = ("C", "D", "B", "A", "C", "B", "D", "A", "B", "C")
    jugar_nivel(preguntas, opciones, respuestas)
   
def nivel_dificil():
    preguntas = (
     "¿Que tipo de ave es el kiwi?: ",
     "¿Que es un palindromo?: ",
     "¿Cuantos dias le toma a la tierra dar una vuelta a la orbita del sol?: ",
     "¿Cual es el pais mas pequeño del mundo?: ",
     "Que pesa mas ¿un kilo de algodon o un kilo de hierro?: ",
     "¿Que artista pinto el techo de la Capilla Sixtina en Roma?: ",
     "¿Quien es la tercera tenista mujer de todos los tiempos en el Grand Slam?: ",
     "¿Cual fue la primera pelicula de Disney?: ",
     "¿Que significa SQL?: ",
     "¿De que color son las cajas negras de los aviones?: ",
     "¿Cuantos meses tienen 28 dias?: ",
     "¿Que es lo que tiene cara, pero no un cuerpo?: ",
     "¿Cual es el pais mas picante del mundo entero?: ",
     "¿Que es lo mas importante para que no te mojes en una tormenta?: ",
     "¿Cuanto duro la famosa guerra de las 100 años?: ",
    )
    opciones = (
    ("A. Es una fruta", "B. No es un ave", "C. Una ave no voladora", "D. Ave de rapiña"),
    ("A. Un tipo de arbol", "B. Palabra del idioma lenca", "C. Figura literaria", "D. Palabra o frase que se lee igual de iquierda a deracha"),  
    ("A. 365", "B. Un dia", "C. 25800", "D. Años luz"),
    ("A. El vaticano", "B. El Salvador", "C. Belice", "D. Monaco"),
    ("A. Un kilo de hierro", "B. Un kilo de algodon", "C. Pesan igual", "D. Todas las anteriores"),
    ("A. Miguel Angel", "B. Picasso", "C. Leonardo Davincci", "D. Vicent Van Gogh"),
    ("A. Anna Kournikova", "B. Serena Williams", "C. Chris Evert", "D. Martina Navratilova"),
    ("A. Mickey Mouse", "B. Petter Pan", "C. Blanca Nieves", "D. Cenicienta"),
    ("A. Secuencia Query Lenguaje", "B. Lenguaje de programacion", "C. Structured Query Language", "D. Secuense Query Language"),
    ("A. Negras", "B. Rojas", "C. Naranja brillante", "D. Neon"),
    ("A. Febrero", "B. Un mes", "C. Todos los meses", "D. Todas las anteriores"),
    ("A. Un busto de escultura", "B. La moneda", "C. Pintura de un rostro", "D. No existen caras sin cuerpo"),
    ("A. Mexico", "B. Corea", "C. Chile", "D. China"),
    ("A. Una sombrilla", "B. Un paragua", "C. Un techo", "D. Que no llueva"),
    ("A. 116 años", "B. 100 años", "C. 101 años", "D. 105 años"),
    )
    respuestas = ("C", "D", "A", "A", "C", "A", "B", "C", "C", "C", "C", "B", "C", "D", "A")
    jugar_nivel(preguntas, opciones, respuestas)

#FUNCIONES AHORCADO
def dibujar_ahorcado(intentos):
    estados = [
        """
           --------
           |      |
                  |
                  |
                  |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
                  |
                  |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
           |      |
                  |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
          /|      |
                  |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
          /|\\     |
                  |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
          /|\\     |
          /       |
                  |
        ============
        """,
        """
           --------
           |      |
           O      |
          /|\\     |
          / \\     |
                  |
        ============
        """
    ]
    errores = 6 - intentos
    indice = min(6, max(0, errores))
    print(estados[indice])

def jugar_ahorcado(nivel): #funcion que inicia el juego del ahorcado
    #Variables
    palabrasNivelFacil = ["GO", "html", "java", "sql", "css", "php", "perl"] #palabras nivel facil
    palabrasNivelMedio = ["rust", "python", "swift", "kotlin", "nosql", "vuejs"] #palabras nivel medio
    palabrasNivelDificil = ["reactnative", "javascript", "typescript", "matlab", "visualbasic"] #palabras nivel dificl

    if nivel == "facil": #define si el nivel es facil
        palabras = palabrasNivelFacil #elige las palabras a enviar
        intentos = 8 #numero de intentos
    elif nivel == "medio": #nivel medio
        palabras = palabrasNivelMedio #palabras nivel medio
        intentos = 6 #numero de intentos
    else: 
        palabras = palabrasNivelDificil #nivel dificil
        intentos = 4 #numero de intentos
        
    palabra_elegida = random.choice(palabras).lower() #elige una de las palabras aleatoriamente y la coloca en minusculas
    letrasAdivinadas = [] #lista donde se guardan las letras adivinadas

    while intentos > 0: #mientras los intentos sean mayores a 0
        palabraMostrada = "" #La palabra mostrada es un string vacio
        for letra in palabra_elegida: #Por cad letra en la palabra elegida
            if letra in letrasAdivinadas: #si la letra que introduce el usuario esta en las letras adivinadas
                palabraMostrada += letra + " " #suma la letra y un espacio
            else:
                palabraMostrada += "_ " #sino muestra un guion bajo y un espacio
        print(f"\n{palabraMostrada}")

        if "_" not in palabraMostrada: #si ya no quedan guiones bajos, significa que adivino la palabra
            eleccion_correcta()#llama la funcion del sonido
            global puntosAhorcado
            puntosAhorcado +=1
            return True #retorna true si el jugador gana
        
        letra = input("Ingresa una letra: ").lower() #pide una letra al usuario
        
        if len(letra) != 1 or not letra.isalpha(): #si el usuario no ingresa nada o ingresa algo que no sea una letra (alfabetica)
            eleccion_incorrecta() #llama el sonido de error
            print("Ingrese una letra válida") #mensaje de error
            continue #continua el programa, no se detiene aunque haya un error
        
        if letra in letrasAdivinadas: #Si la letra que introduce el usuario ya la habia colocado anteriormente
            eleccion_incorrecta() #llama sonido de error
            print("Ya has usado esa letra, intenta de nuevo") #mensaje de error
            continue #continua, no se detiene
        
        letrasAdivinadas.append(letra) #guarda las letras correctas en la lista
        
        if letra not in palabra_elegida: #si la letra no esta en la palabra elegida
            eleccion_incorrecta() #sonido de error
            intentos -= 1 #quita un intento
            print(f"Letra incorrecta, te quedan {intentos} intentos") #mensaje de intentos
            dibujar_ahorcado(intentos) #dibuja las imagenes del ahorcado
    GameOver()
    print(f"¡¡Perdiste!! La palabra secreta era: {palabra_elegida}") #Si el usuario no adivina la palabra
    return False #retorna falso ya que perdio


##COMIENZA EL PROGRAMA
controlar_musica() #Llama la funcion para controlar la musica
print("")
bienvenido = pyfiglet.figlet_format(text="Juegos de consola", font="big", width=1000) #Fuente de inicio
while True:
    print("")
    validarSeleccion = False #Variable para validar si es una opcion basica
    while validarSeleccion == False: #Menú
        try: #manejo de excepciones
            print(bienvenido)
            eleccion = int(input(f"{" "*10}1.Jugar{" "*10}2.Tablero de puntuaciones{" "*10}3.Salir\n{" "*31}Su elección: ")) #pide una eleccion
            print("")
            if eleccion >0 and eleccion <=5: #Si la opcion esta entre este rango es valido
                controlar_sonidos() #sonido de feedback
                validarSeleccion = True
            else:
                eleccion_incorrecta()
                print("Ingrese un valor de los mostrados en el menú\n")
                time.sleep(1) #timer 
                os.system('cls') #limpia la consola
        except ValueError:
            print("")
            print("El valor ingresado no es un número") #Manejo de excepciones 
            print("")
        time.sleep(1) #timer 
        os.system('cls') #limpia la consola 
    if eleccion == 1: #Sesion de juego
        while True:
            archivocsv = "tablaPuntuacion.csv"
            print(bienvenido)
            usuario = input(f"{" "*20}Ingrese un nombre de usuario: ") #pide un nombre de usuario para diferenciarlos
            controlar_sonidos()
            if verificarUsuario(archivocsv, usuario):
                respuesta = input(f"{" "*10}El usuario '{usuario}' ya existe. ¿Deseas continuar? (s/n): ").lower()
                if respuesta == "s":
                    print("")
                    print(f"{" "*25}Bienvenido de vuelta!")
                    print("")
                    time.sleep(1) #timer 
                    os.system('cls') #limpia la consola 
                    break
                else:
                    time.sleep(1) #timer 
                    os.system('cls') #limpia la consola 
                    
            else:
                time.sleep(1) #timer 
                os.system('cls') #limpia la consola 
                break              
        
        while True: #BUCLE DE LA SESION
            while True: #BUCLE DE MENU
                print(bienvenido)
                try: #manejo de excepciones
                    opcion = int(input(f"1.Adivinanza de números!{" "*10}2.Piedra Papel o Tijeras!{" "*10}3.Preguntas y Respuestas!{" "*10}4.Ahorcado{" "*10}5.Salir\n{" "*40}Su Elección: ")) #pide una eleccion
                    controlar_sonidos() #llama funcion de sonidos
                    print("")
                    if opcion >0 and opcion <=5: #verificacion que este dentro de este rango
                        break #si esta en el rango se sale del bucle
                    else: #sino, pide la opcion de nuevo
                        print("Ingrese un valor de los mostrados en el menú\n")
                except ValueError: #manejo de excepciones
                    eleccion_incorrecta()
                    print("")
                    print("El valor ingresado no es un número")
                    print("")
                    time.sleep(1) #timer 
                    os.system('cls') #limpia la consola
            time.sleep(1) #temporizador de 1 segundo
            os.system('cls') #limpia la consola
            if opcion == 1: #si la opcion del usuario es 1
                juego = "AdivinanzaDeNumeros.csv" #da el nombre que tendra el archivo csv
                try:
                    with open("AdivinanzaDeNumeros.csv", encoding="utf-8") as archivo: #toma los datos y los coloca en una lista
                        datos=list(csv.DictReader(archivo,delimiter=","))
                        mostrarTabla(datos) #llamamos la funcion para mostrar los datos
                except Exception as mensaje:
                    print(mensaje) #mensaje de error
                    
                menu_principal() #funcion de adivinanza de numeros
                crearTabladeJuego(usuario,puntosNumRandom,juego)
                crearTablaDePuntuacion(usuario,puntosNumRandom,puntosPPT,puntosPyR,puntosAhorcado)
                puntosNumRandom = 0
            elif opcion == 2: #si la opcion es 2, entra a piedra papel o tijeras
                print(f"¡Ha elegido Piedra, Papel o Tijeras!")
                juego = "PiedraPapelTijera.csv"
                try:
                    with open("PiedraPapelTijera.csv", encoding="utf-8") as archivo:
                        datos=list(csv.DictReader(archivo,delimiter=","))
                        mostrarTabla(datos)
                except Exception as mensaje:
                    print(mensaje)
                while True:
                    print("Jugarás 3 rondas. Necesitas ganar al menos 2 para obtener 1 punto.\n")

                    rondas = 0
                    ganadas = 0

                    while rondas < 3:
                        print("1: Piedra")
                        print("2: Papel")
                        print("3: Tijera")
                        try:
                            jugador = int(input("Elige tu opción (1-3): "))

                            if jugador not in (1, 2, 3):
                                print("Opción inválida. Por favor, elige un número entre 1 y 3.\n")
                                continue  # No cuenta como ronda

                            time.sleep(0.5)
                            print("Has elegido:", traducir(jugador))
                            pc = random.choice((1, 2, 3))
                            print("Pc eligió:", traducir(pc))

                            if jugador == 2 and pc == 1:
                                eleccion_correcta()
                                print("Ganaste la ronda: el papel envuelve a la piedra")
                                ganadas += 1
                            elif jugador == 3 and pc == 2:
                                eleccion_correcta()
                                print("Ganaste la ronda: la tijera corta papel")
                                ganadas += 1
                            elif jugador == 1 and pc == 3:
                                eleccion_correcta()
                                print("Ganaste la ronda: la piedra rompe tijera")
                                ganadas += 1
                            elif jugador == 1 and pc == 2:
                                eleccion_incorrecta()
                                print("Perdiste la ronda: el papel envuelve a la piedra")
                            elif jugador == 2 and pc == 3:
                                eleccion_incorrecta()
                                print("Perdiste la ronda: la tijera corta papel")
                            elif jugador == 3 and pc == 1:
                                eleccion_incorrecta()
                                print("Perdiste la ronda: la piedra rompe tijera")
                            elif jugador == pc:
                                eleccion_incorrecta()
                                print("Empate, seleccionaron el mismo objeto")

                            rondas += 1
                            print(f"Rondas jugadas: {rondas}/3")
                            print("-" * 40)

                        except ValueError:
                            print("El valor ingresado no es un número válido\n")
                            continue

                    # Resultado final de la partida
                    print("\nResultado de la partida:")
                    if ganadas >= 2:
                        print("¡Ganaste la partida! (+1 punto)")
                        puntosPPT = 1
                    else:
                        GameOver()
                        print("No ganaste la partida. (+0 puntos)")
                        puntosPPT = 0

                    repetir = input("¿Deseas jugar otra partida? (s/n): ").lower()
                    if repetir == 's':
                        input("\nPresiona Enter para comenzar otra partida...")
                    else:
                        fin = pyfiglet.figlet_format(text="Gracias por jugar", font="big", width=1000)
                        time.sleep(1) #timer 
                        os.system('cls') #limpia la consola
                        break
                crearTabladeJuego(usuario,puntosPPT,juego)
                crearTablaDePuntuacion(usuario,puntosNumRandom,puntosPPT,puntosPyR,puntosAhorcado)
                puntosPPT = 0
            elif opcion == 3: #Si la opcion es 3, entra al juego de trivia
                juego = "Trivia.csv"
                try:
                    with open("Trivia.csv", encoding="utf-8") as archivo:
                        datos=list(csv.DictReader(archivo,delimiter=","))
                        mostrarTabla(datos)
                except Exception as mensaje:
                    print(mensaje)
                while True:
                    print("\n====== MENÚ DE TRIVIA ======")
                    print("1. Nivel Fácil")
                    print("2. Nivel Intermedio")
                    print("3. Nivel Difícil")
                    print("4. Salir")
                    print("\n============================")
                    try: #para uso de excepcion
                        opcion_menu = int(input("Seleccione una opción: "))
                    
                        if opcion_menu == 1:
                            print("\n=================================== Bienvenido al nivel FACIL del juego TRIVIA ===================================")
                            print("Si deseas SALIR antes de terminar toda la ronda de preguntas puedes escribir SALIR en vez de la opcion de respuesta")
                            print("_"*115)
                            nivel_facil()
                        elif opcion_menu == 2:
                            print("\n=================================== Bienvenido al nivel INTERMEDIO del juego TRIVIA ===================================")
                            print("Si deseas SALIR antes de terminar toda la ronda de preguntas puedes escribir SALIR en vez de la opcion de respuesta")
                            print("_"*115)
                            nivel_medio()
                        elif opcion_menu == 3:
                            print("\n=================================== Bienvenido al nivel DIFICIL del juego TRIVIA ===================================")
                            print("Si deseas SALIR antes de terminar toda la ronda de preguntas puedes escribir SALIR en vez de la opcion de respuesta")
                            print("_"*115)
                            nivel_dificil()
                        elif opcion_menu == 4:
                            print("¡Hasta la próxima!")
                            break
                        else:
                            print("ERROR!!!! Ingrese un valor válido (1-4)...") #validacion de solo ingreso de las opciones del menu si el usuario escribe otro numero no podra ingresar al menu
                            continue  # vuelve al menú principal sin preguntar si desea repetir

                        repetir = input("\n¿Desea jugar otro nivel? (S/N): ").upper() #variable para pregunat al usuario si desea continuar al siguiente nivel o volver al menu
                        if repetir != "S":
                            print("¡Gracias por participar!") #COn este mensaje regresa al menu de todos los juegos 
                            time.sleep(1) #timer 
                            os.system('cls') #limpia la consola
                            break
                    except ValueError: #excepcion que permitira que el usuario ingrese solo numeros y no letras
                        print("Debes ingresar un numero de las opciones no puedes ingresar letras")
                crearTablaDePuntuacion(usuario,puntosNumRandom,puntosPPT,puntosPyR,puntosAhorcado)
                crearTabladeJuego(usuario,puntosPyR,juego)
                puntosPyR = 0
            
            elif opcion == 4: #Si la opcion es 4, entra al ahorcado
                nivelActual = "facil" #define el nivel actual
                juego = "Ahorcado.csv" #da nombre para el archivo csv
                print(f"¡Bienvenido al juego del Ahorcado!")
                print(f"Pistas: Las palabras estan relacionadas a lenguajes de programación!")
                print(f"Obtienes un punto al adivinar las 3 palabras correctamente")
                print(f"Para el nivel facil tienes 8 intentos, en el medio tienes 6 intentos y para el dificil tienes 4 intentos")
                print(f"¡Mucha suerte!")
                try: #manejo de excepciones
                    with open("Ahorcado.csv", encoding="utf-8") as archivo: #abre el archivo
                        datos=list(csv.DictReader(archivo,delimiter=",")) #lo lee usando las comas como separador
                        mostrarTabla(datos) #llama la funcion que muestra la tabla
                except Exception as mensaje:
                    print(mensaje) #si hay error lo muestra
                while True: #bucle del juego
                    if jugar_ahorcado(nivelActual): #usa el nivel facil que definimos antes
                        if nivelActual == "facil": #si el nivel el facil
                            nivelActual = "medio" #lo cambia a medio
                            print("Felicidades, pasaste a nivel medio!") #mensaje de felicitation
                        elif nivelActual == "medio": #si el nivel es medio
                            nivelActual = "dificil" #pasa a dificil
                            print("Felicidades, pasaste a nivel dificil!") #mensaje de felicitacion
                        else:
                            print("Felicidades, completaste todos los niveles! Obstuviste un punto") #Si pasa el nivel dificil da mensaje de felicitacion
                            continuar = input("¿Deseas jugar de nuevo? (s/n): ").lower() #pregunta si quiere jugar de nuevo
                            if continuar != "s": #si es diferente de "s" imprime una tabla de puntaje
                                fin = pyfiglet.figlet_format(text="Gracias por jugar", font="big", width=1000) #mensaje de fin
                                time.sleep(1) #timer 
                                os.system('cls') #limpia la consola
                                nivelActual ="facil"
                                break
                    else:
                        continuar = input("¿Deseas jugar de nuevo? (s/n): ").lower() #pregunta si quiere jugar de nuevo
                        if continuar != "s": #si es diferente de "s" imprime una tabla de puntaje
                            fin = pyfiglet.figlet_format(text="Gracias por jugar", font="big", width=1000)
                            time.sleep(1) #timer 
                            os.system('cls') #limpia la consola
                            break
                        nivelActual ="facil"
                crearTablaDePuntuacion(usuario,puntosNumRandom,puntosPPT,puntosPyR,puntosAhorcado)
                crearTabladeJuego(usuario,puntosAhorcado,juego) #llama la funcion de crear tabla de juego
                puntosAhorcado = 0
            elif opcion == 5: #si la opcion es 5 (salir)
                puntosTotales = puntosNumRandom + puntosPPT + puntosPyR + puntosAhorcado
                datoPuntos.append([usuario, puntosNumRandom, puntosPPT, puntosPyR, puntosAhorcado, puntosTotales]) #guarda los datos en la tabla y regresa a 0 las variables
                
                puntosPPT = 0
                puntosNumRandom = 0
                puntosPyR = 0
                puntosAhorcado = 0
                break #sale del bucle

    elif eleccion ==2: #Tablero de puntuación
        mostrarTablaPuntuacion()
        
    elif eleccion == 3: #si selecciona 3 (salir) se sale del bucle
        pygame.mixer.music.stop()
        print("")  
        fin = pyfiglet.figlet_format(text="Gracias por jugar", font="big", width=1000) #Fuente de inicio   
        print(fin) #mensaje de feedback
        GraciasPorJugar()
        time.sleep(3) #timer 
        break
    else:
        eleccion_incorrecta() #sonido de error
        print("Opción no válida") #mensaje de error
        print("")
        