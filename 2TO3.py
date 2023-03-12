import sqlite3

conexion = sqlite3.connect('databases/basesDeDatosIncidencias.db')
cursor = conexion.cursor()
cursor.execute("ALTER TABLE bd_bloqueos ADD COLUMN DESDE TEXT")
cursor.execute("ALTER TABLE bd_bloqueos ADD COLUMN HASTA TEXT")
conexion.commit()
conexion.close

# Conectarse a la base de datos
conexion = sqlite3.connect('databases/basesDeDatosIncidencias.db')

# Crear un objeto cursor
cursor = conexion.cursor()

# Verificar si la columna existe en la tabla
cursor.execute("PRAGMA table_info('bd_bloqueos')")
columnas = [columna[1] for columna in cursor.fetchall()]

if 'DESDE' in columnas:
    print('La columna DESDE ha sido añadida exitosamente')
else:
    print('La columna DESDE no existe en la tabla')

if 'HASTA' in columnas:
    print('La columna HASTA ha sido añadida exitosamente')
else:
    print('La columna HASTA no existe en la tabla')
    
# Cerrar la conexión
conexion.close()
