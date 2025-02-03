import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Definir los valores a insertar
ano = 2025
fecha_inicio = "2025-03-01"
fecha_fin = "2025-12-15"
user_id = 1  # Asegúrate de que este usuario exista en auth_user

# Insertar la fila en la tabla
query = """
INSERT INTO gestion_anolectivo (ano, fecha_inicio, fecha_fin, user_id)
VALUES (?, ?, ?, ?)
"""
cursor.execute(query, (ano, fecha_inicio, fecha_fin, user_id))

# Guardar los cambios y cerrar conexión
conn.commit()
conn.close()

print("Fila insertada correctamente.")
