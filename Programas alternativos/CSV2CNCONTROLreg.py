import sqlite3
# Abre el archivo ARC.csv
ARCHIVO = open("ARC.csv", "r")
# A la variable TOTAL le damos el total de registros de ARCHIVO
contenido = ARCHIVO.read()
TOTAL = len(contenido.splitlines())
# Cerramos ARCHIVO
ARCHIVO.close()
# Abre el archivo ARC.csv
ARCHIVO = open("ARC.csv", "r")

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_registros (
        USUARIO         text,
        FECHA           text,
        DESCRIPCION     text,
        ORIGEN          text,
        HORA            text,
        PRODUCTO        text,
        FUENTE          text,
        NOTAS           text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

    # Cerrar conexion 
    base_datos_datos.close()
    
except:
    
    pass

# Creamos una variable COUNT para contar las lineas
COUNT = 0
# Crea un bucle para leer todas las lineas de ARCHIVO
for LINEA in ARCHIVO:
    # Sumamos 1 a COUNT
    COUNT = COUNT + 1
    
    # Escribimos el número de linea sobre el total
    print("Leyendo linea " + str(COUNT) + " de " + str(TOTAL))
          
    # Convierte la LINEA en una lista
    LISTA = LINEA.split(",")
    
    # Pinta la lista
    FECHA       = LISTA[2]
    DESCRIPCION = LISTA[3]
    ORIGEN      = LISTA[4]
    HORA        = LISTA[6]
    USUARIO     = LISTA[9]
    TIPOLOGIA   = LISTA[10]
    FUENTE      = LISTA[11]
    NOTAS       = LISTA[12]

    
    # FECHA es dd/mm/yy y lo convertimos en yyyy/mm/dd
    LISTA_FECHA = FECHA.split("/")
    DIA         = LISTA_FECHA[0]
    MES         = LISTA_FECHA[1]
    ANIO        = LISTA_FECHA[2]
    FECHA       = "20" + ANIO + "/" + MES + "/" + DIA
        
    # si DESCRIPCION es: GENERAL se convierte en General
    if DESCRIPCION == "GENERAL":
        DESCRIPCION = "General"
    # si DESCRIPCION es: NENS DE 9 A 15 ANYS se convierte en menor 15
    if DESCRIPCION == "NENS DE 9 A 15 ANYS":
        DESCRIPCION = "menor 15"
    # si DESCRIPCION es: MAJORS DE 65 ANYS se convierte en major 65
    if DESCRIPCION == "MAJORS DE 65 ANYS":
        DESCRIPCION = "major 65"
    # si DESCRIPCION es: PROFESSORS / GUIES / PERIODISTES se convierte en Professor
    if DESCRIPCION == "PROFESSORS / GUIES / PERIODISTES":
        DESCRIPCION = "Professor"
    # si DESCRIPCION es: SENSE TREBALL se convierte en Atur
    if DESCRIPCION == "SENSE TREBALL":
        DESCRIPCION = "Atur"
    # si DESCRIPCION es: CARNET ESTUDIANT se convierte en Estudiant
    if DESCRIPCION == "CARNET ESTUDIANT":
        DESCRIPCION = "Estudiant"
    # si DESCRIPCION es: CLUB SUPER 3 se convierte en Club Super3
    if DESCRIPCION == "CLUB SUPER 3":
        DESCRIPCION = "Club Super3"
    # si DESCRIPCION es: FAMILIA NUMBROSA O MONOPARENTAL se convierte en Fam. nombrosa
    if DESCRIPCION == "FAMILIA NUMBROSA O MONOPARENTAL":
        DESCRIPCION = "Fam. nombrosa"
    # si DESCRIPCION es: DISCAPACITAT se convierte en Discapacitat
    if DESCRIPCION == "DISCAPACITAT":
        DESCRIPCION = "Discapacitat"
    # si DESCRIPCION es: MENORS DE 8 ANYS se convierte en menor 8 
    if DESCRIPCION == "MENORS DE 8 ANYS":
        DESCRIPCION = "menor 8"
    # si DESCRIPCION es: INVITACIÓ se convierte en Invitació
    if DESCRIPCION == "INVITACIÓ":
        DESCRIPCION = "Invitació"
    # si DESCRIPCION es: CARNET JOVE se convierte en Carnet Jove
    if DESCRIPCION == "CARNET JOVE":
        DESCRIPCION = "Carnet Jove"
    # si DESCRIPCION es: VISIT REUS GENERAL se convierte en General
    if DESCRIPCION == "VISIT REUS GENERAL":
        DESCRIPCION = "General"
    # si DESCRIPCION es: VISIT REUS REDUÏDA se convierte en major 65
    if DESCRIPCION == "VISIT REUS REDUÏDA":
        DESCRIPCION = "major 65"
    # si DESCRIPCION es: FOTOGRAFICA se convierte en General
    if DESCRIPCION == "FOTOGRAFICA":    
        DESCRIPCION = "General"
    # si DESCRIPCION es: INFANTILS se convierte en menor 15
    if DESCRIPCION == "INFANTILS":
        DESCRIPCION = "menor 15"
    # si DESCRIPCION es: ESCOLAR INFANTIL se convierte en menor 8
    if DESCRIPCION == "ESCOLAR INFANTIL":
        DESCRIPCION = "menor 8"
    # si DESCRIPCION es: ESCOLAR MITJANS se convierte en menor 15
    if DESCRIPCION == "ESCOLAR MITJANS":
        DESCRIPCION = "menor 15"
    # si DESCRIPCION es: ESCOLAR GRANS se convierte en menor 15
    if DESCRIPCION == "ESCOLAR GRANS":
        DESCRIPCION = "menor 15"
    # si DESCRIPCION es: ESCOLAR ANTIGA se convierte en menor 15 
    if DESCRIPCION == "ESCOLAR ANTIGA":
        DESCRIPCION = "menor 15"
                                           
    
    # si USUARIO es:  BENJAMÍN se convierte en BENJAMI
    if USUARIO == "BENJAMÍN":
        USUARIO = "BENJAMI"
    # si USUARIO es:  MANUEL se convierte en MANU
    if USUARIO == "MANUEL":
        USUARIO = "MANU"
    # si USUARIO es:  DANIEL se convierte en DANI
    if USUARIO == "DANIEL":
        USUARIO = "DANI"
    # si USUARIO es: PILAR se convierte en PILI
    if USUARIO == "PILAR":
        USUARIO = "PILI"
            
    # si TIPOLOGIA es: ESCAPE ROOM se convierte en ESCOLAR ESCAPE ROOM
    if TIPOLOGIA == "ESCAPE ROOM":
        TIPOLOGIA = "ESCOLAR ESCAPE ROOM"
    # si TIPOLOGIA es: PREMIUM se convierte en PRÈMIUM
    if TIPOLOGIA == "PREMIUM":  
        TIPOLOGIA = "PRÈMIUM"
    # si TIPOLOGIA es:  FOTOGRAFICA se convierte en FOTOGRÀFIA
    if TIPOLOGIA == "FOTOGRAFICA":
        TIPOLOGIA = "FOTOGRÀFIA"
    # si TIPOLOGIA es: INFANTIL se convierte en ESCOLAR JARDÍ MÀGIC
    if TIPOLOGIA == "INFANTIL":
        TIPOLOGIA = "ESCOLAR JARDÍ MÀGIC"
    # si TIPOLOGIA es: ESCOLAR se convierte en ESCOLAR SIMPLE
    if TIPOLOGIA == "ESCOLAR":
        TIPOLOGIA = "ESCOLAR SIMPLE"

    # si FUENTE es:  XARXES SOCIALS se convierte en Xarxes socials
    if FUENTE == "XARXES SOCIALS":
        FUENTE = "Xarxes socials"
    # si FUENTE es:  APARADORS se convierte en Aparadors
    if FUENTE == "APARADORS":
        FUENTE = "Aparadors"
    # si FUENTE es:  RECOMANAT se convierte en Recomanat
    if FUENTE == "RECOMANAT":    
        FUENTE = "Recomanat"
    # si FUENTE es:  RÀDIO se convierte en Ràdio
    if FUENTE == "RÀDIO":
        FUENTE = "Ràdio"
    # si FUENTE es:  TELEVISIÓ se convierte en Televisió
    if FUENTE == "TELEVISIÓ":
        FUENTE = "Televisió"
    # si FUENTE es:  BUSTIA se convierte en Bustia
    if FUENTE == "BUSTIA":
        FUENTE = "Bustia"
    # si FUENTE es:  OFICINA DE TURISME se convierte en Oficina de turisme 
    if FUENTE == "OFICINA DE TURISME":
        FUENTE = "Oficina de turisme"
    # si FUENTE es:  INTERNET BUSCANT INFO DE REUS se convierte en Internet
    if FUENTE == "INTERNET BUSCANT INFO DE REUS":    
        FUENTE = "Internet"
    # si FUENTE es:  INTERNET se convierte en Internet
    if FUENTE == "INTERNET":
        FUENTE = "Internet"
    # si FUENTE es:  PASSEJANT PER REUS se convierte en Passejant per Reus
    if FUENTE == "PASSEJANT PER REUS":
        FUENTE = "Passejant per Reus"
    # si FUENTE es:  DIARI se convierte en Premsa
    if FUENTE == "DIARI":
        FUENTE = "Premsa"
    # si FUENTE es:  VISITA PENDENT se convierte en Visita pendent
    if FUENTE == "VISITA PENDENT":
        FUENTE = "Visita pendent"
    # si FUENTE es:  REPETIDORS se convierte en Repetidor
    if FUENTE == "REPETIDORS":
        FUENTE = "Repetidor"
    # si FUENTE es:  INTERÈS CULTURAL se convierte en Interés cultural
    if FUENTE == "INTERÈS CULTURAL":
        FUENTE = "Interès cultural"
    # si FUENTE es:  M'HA SURTIT DE LA FIGA se convierte en No ho vol dir
    if FUENTE == "M'HA SURTIT DE LA FIGA":
        FUENTE = "No ho vol dir"
    # si FUENTE es:  FLYERS se convierte en Flyers
    if FUENTE == "FLYERS":
        FUENTE = "Flyers"
        
    # Salva datos
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosRegistros.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()   
    
    # Inserta en la base de tados
    cursor.execute("""INSERT INTO bd_registros VALUES (:usuario, :fecha,
                :descripcion, :origen, :hora, :producto, :fuente, :notas)""",
                {
                    'usuario':      USUARIO,
                    'fecha':        FECHA,
                    'descripcion':  DESCRIPCION,
                    'origen':       ORIGEN,
                    'hora':         HORA,
                    'producto':     TIPOLOGIA,
                    'fuente':       FUENTE,
                    'notas':        NOTAS
                    })


    # Asegura los cambios
    base_datos_datos.commit()

    # Cerrar conexion 
    base_datos_datos.close()
    
# Cerramos ARCHIVO
ARCHIVO.close()
