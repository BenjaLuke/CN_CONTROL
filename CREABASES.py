import sqlite3                                          # Para trabajar con la base de datos

# ------------------------------ Bases de datos -------------------------------

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosDatos.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos las tablas (en caso de que existan saltarán este paso)

try:
    cursor.execute("""CREATE TABLE bd_productos (
        NOM             text,
        PREU_HABITUAL   text,
        PREU_ACTUAL     text,
        REGISTRABLE     text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

try:
    cursor.execute("""CREATE TABLE bd_usuarios (
        NOM             text,
        CLAVE           text,
        NIVEL           text,
        INGLES          text,
        CASTELLANO      text,
        CATALAN         text,
        FRANCES         text,
        HORASMES        text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass


# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosClientes.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

try:
    cursor.execute("""CREATE TABLE bd_clientes (
        NOM             text,
        DIRECCION1      text,
        DIRECCION2      text,
        DIRECCION3      text,
        TELEFONO        text,
        MAIL            text,
        NIFCIF          text,
        CONTACTO        text,
        TELCONTACTO     text,
        MAILCONTACTO    text)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

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

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

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

except:
    
    pass

try:
    cursor.execute("""CREATE TABLE bd_bloqueos (
        FECHA           text,
        DESDE           text,
        HASTA           text,
        MOTIVO          text,)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()

# Creamnos la base de datos o conectamos con ella si ya existe
base_datos_datos = sqlite3.connect('databases/basesDeDatosProforma.db')

# Creamos el cursor
cursor = base_datos_datos.cursor()   

# Creamos la tabla (en caso de que exista saltará este paso)

try:
    cursor.execute("""CREATE TABLE bd_Proforma (
        FECHA           text,
        FECHA_PRO       text,
        NUM_PRO         text,
        CLIENTE         text,
        CANT_1          text,
        CONCEPT_1       text,
        PRECIO_1        text,
        CANT_2          text,
        CONCEPT_2       text,
        PRECIO_2        text,
        IVA             text,
        TIPO_IVA        text,
        INCLUIDO_IVA    text,
        ID_INCIDENCIA   text,
        PARTE           text,)""")
    
    # Ejecutar (commit) instrucción o consulta
    base_datos_datos.commit()

except:
    
    pass

# Cierra la conexión con la base de datos
base_datos_datos.close()
