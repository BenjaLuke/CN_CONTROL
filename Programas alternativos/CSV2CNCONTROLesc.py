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
base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_incidencias (
        FECHA           text,
        HORA            text,
        PAX1            text,
        PAX2            text,
        PRODUCTO        text,
        IDIOMA          text,
        TEL_EXTRA       text,
        ESTADO          text,
        USUARIO         text,
        FECHA_CREA      text,
        CLIENTE         text,
        MAIL_EXTRA      text,
        PRECIO1         text,
        TIPO1           text,
        PRECIO2         text,
        TIPO2           text,
        AGENDADO        text,
        FECHA_REV       text,
        PAGAT           text,
        NOTAS           text,
        FACTURA         text,
        CONTACTO        text)""")
    
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
    FECHA       = LISTA[7]
    HORA        = LISTA[5]
    PAX1        = LISTA[4]
    IDIOMA      = LISTA[9]
    TEL_EXTRA   = LISTA[2]
    ESTADO      = LISTA[14]
    USUARIO     = LISTA[0]
    FECHA_CREA  = LISTA[6]
    CLIENTE     = LISTA[1]
    MAIL_EXTRA  = LISTA[3]
    AGENDADO    = LISTA[10]
    PAGAT       = LISTA[8]
    NOTAS       = LISTA[11]
    FACTURA     = LISTA[15]
    PAX2        = LISTA[16]
        
    # Salva datos
    # Crea la base de datos o conecta con ella
    base_datos_datos = sqlite3.connect('databases/basesDeDatosIncidencias.db')
        
    # Crea el cursor
    cursor = base_datos_datos.cursor()   
    
    # Inserta en la base de tados
    cursor.execute("""INSERT INTO bd_incidencias VALUES (:fecha, :hora,
                :pax1, :pax2, :producto, :idioma, :tel_extra, :estado, :usuario, :fecha_crea, :cliente, :mail_extra, :precio1, :tipo1, :precio2, :tipo2, :agendado, :fecha_rev, :pagat, :notas, :factura, :contacto)""",
                {
                    'fecha':        FECHA,
                    'hora':         HORA,
                    'pax1':         PAX1,
                    'pax2':         PAX2,
                    'producto':     "",
                    'idioma':       IDIOMA,
                    'tel_extra':    TEL_EXTRA,
                    'estado':       ESTADO,
                    'usuario':      USUARIO,
                    'fecha_crea':   FECHA_CREA,
                    'cliente':      CLIENTE,
                    'mail_extra':   MAIL_EXTRA,
                    'precio1':      "",
                    'tipo1':        "",
                    'precio2':      "",
                    'tipo2':        "",
                    'agendado':     AGENDADO,
                    'fecha_rev':    "",
                    'pagat':        PAGAT,
                    'notas':        FACTURA,
                    'factura':      NOTAS,
                    'contacto':     ""
                    })


    # Asegura los cambios
    base_datos_datos.commit()

    # Cerrar conexion 
    base_datos_datos.close()
    
# Cerramos ARCHIVO
ARCHIVO.close()
