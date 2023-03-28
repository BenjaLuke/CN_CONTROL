import sqlite3

conexion = sqlite3.connect('databases/basesDeDatosDatos.db')
cursor = conexion.cursor()
# Añade una columna a la tabla bd_usuarios con valor "160"
cursor.execute("ALTER TABLE bd_usuarios ADD COLUMN HORASMES TEXT")
# cursor.execute("ALTER TABLE bd_bloqueos ADD COLUMN HASTA TEXT")
conexion.commit()
conexion.close

# Conectarse a la base de datos
conexion = sqlite3.connect('databases/basesDeDatosProforma.db')

# Crear un objeto cursor
cursor = conexion.cursor()

# Verificar si la columna existe en la tabla
cursor.execute("PRAGMA table_info('bd_usuarios')")
columnas = [columna[1] for columna in cursor.fetchall()]

if 'HORASMES' in columnas:
    print('La columna HORASMES ha sido añadida exitosamente')
else:
    print('La columna HORASMES no existe en la tabla')
'''
if 'HASTA' in columnas:
    print('La columna HASTA ha sido añadida exitosamente')
else:
    print('La columna HASTA no existe en la tabla')
'''    
# Cerrar la conexión
conexion.close()
# Vuelve a abrir la tabla
