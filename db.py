import sqlite3
from datetime import datetime

def inicializar_bd():
    conn = sqlite3.connect("monitor_mind.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tiempo_total REAL,
        aciertos INTEGER,
        errores INTEGER,
        omisiones INTEGER,
        igap REAL,
        capacidad_perceptiva REAL,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def insertar_resultado(tiempo_total, aciertos, errores, omisiones, igap, capacidad_perceptiva):
    conn = sqlite3.connect("monitor_mind.db")
    cursor = conn.cursor()
    
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Obtener la fecha y hora actual
    
    cursor.execute("""
    INSERT INTO resultados (tiempo_total, aciertos, errores, omisiones, igap, capacidad_perceptiva, fecha)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tiempo_total, aciertos, errores, omisiones, igap, capacidad_perceptiva, fecha_actual))
    
    conn.commit()
    conn.close()

# Llamar a la función para asegurarnos de que la tabla está creada
inicializar_bd()

# Llamar a la función de inserción
insertar_resultado(10.5, 5, 2, 1, 0.8, 2.5)
