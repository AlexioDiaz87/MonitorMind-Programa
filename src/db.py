import psycopg2
import hashlib
import os

# Configuración de la conexión a PostgreSQL
DATABASE = "Mind"
USER = "postgres"
PASSWORD = "1234"
HOST = "localhost"
PORT = "5432"

# Archivo donde guardaremos la sesión del usuario
SESSION_FILE = "sesion.txt"

def get_connection():
    """Establece y retorna una conexión a la base de datos."""
    return psycopg2.connect(
        dbname=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

def guardar_sesion(idUser):
    """Guarda el idUser en un archivo para persistencia."""
    with open(SESSION_FILE, "w") as f:
        f.write(str(idUser))

def obtener_usuarios():
    """Obtiene la lista de usuarios registrados en la base de datos PostgreSQL"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idUser, usuario FROM users")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios  # Retorna una lista de tuplas (idUser, usuario)

def obtener_resultados_usuario(idUser):
    """Obtiene los resultados del usuario seleccionado"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idResult, porcentaje_fatiga1, porcentaje_fatiga2, capacidad_perceptiva, resultado_final FROM resultados WHERE idUser = %s", (idUser,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados  # Retorna una lista de resultados

def eliminar_usuario(idUser):
    """Elimina un usuario y sus resultados asociados"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM resultados WHERE idUser = %s", (idUser,))  # Elimina resultados primero
        cursor.execute("DELETE FROM users WHERE idUser = %s", (idUser,))  # Luego elimina el usuario
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar usuario: {e}")
    finally:
        cursor.close()
        conn.close()

def cargar_sesion():
    """Carga el idUser de la sesión guardada en el archivo."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return int(f.read().strip())
    return None  # Retorna None si no hay sesión activa

def cerrar_sesion():
    """Elimina la sesión guardada."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def inicializar_bd():
    """Crea las tablas users y resultados si no existen."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            idUser SERIAL PRIMARY KEY,
            usuario VARCHAR(255) UNIQUE NOT NULL,
            contraseña VARCHAR(255) NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            idResult SERIAL PRIMARY KEY,
            idUser INT REFERENCES users(idUser),
            porcentaje_fatiga1 FLOAT,
            porcentaje_fatiga2 FLOAT,
            capacidad_perceptiva FLOAT,
            resultado_final FLOAT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def hashear_contrasena(contrasena):
    """Devuelve la contraseña encriptada usando SHA-256."""
    return hashlib.sha256(contrasena.encode()).hexdigest()

def verificar_credenciales(usuario, contrasena):
    """Verifica si las credenciales son correctas y retorna el idUser."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT idUser, contraseña FROM users WHERE usuario = %s", (usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado is None:
        return None  # Usuario no encontrado
    if resultado[1] == hashear_contrasena(contrasena):
        return resultado[0]  # Retorna el idUser si la contraseña es correcta
    return None  # Contraseña incorrecta

def registrar_usuario_db(usuario, contrasena):
    """Registra un nuevo usuario en la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (usuario, contraseña) VALUES (%s, %s)",
            (usuario, hashear_contrasena(contrasena))
        )
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def guardar_resultado(idUser):
    """Obtiene o crea un registro de resultados para un usuario en la sesión actual."""
    conn = get_connection()
    cursor = conn.cursor()

    # Intentar obtener el último resultado del usuario
    cursor.execute("SELECT idResult FROM resultados WHERE idUser = %s ORDER BY idResult DESC LIMIT 1", (idUser,))
    resultado_existente = cursor.fetchone()

    if resultado_existente:
        idResult = resultado_existente[0]  # Usar el último idResult existente
    else:
        # Si no hay registro previo, insertar uno nuevo
        cursor.execute("INSERT INTO resultados (idUser) VALUES (%s) RETURNING idResult", (idUser,))
        idResult = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()
    
    return idResult

def actualizar_resultado_final(idResult, resultado_formula):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el ID de resultado existe antes de actualizar
    cursor.execute("SELECT idresult FROM resultados WHERE idresult = %s", (idResult,))
    existe = cursor.fetchone()

    if existe:
        cursor.execute(
            "UPDATE resultados SET resultado_final = %s WHERE idresult = %s",
            (resultado_formula, idResult)
        )
        conn.commit()
    else:
        print("⚠ No se encontró el resultado en la BD, no se pudo actualizar.")

    conn.close()


def actualizar_fatiga1(idResult, porcentaje_fatiga1):
    """Actualiza el porcentaje de fatiga1 en un resultado existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE resultados SET porcentaje_fatiga1 = %s WHERE idResult = %s",
        (porcentaje_fatiga1, idResult)
    )
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_fatiga2(idResult, porcentaje_fatiga2):
    """Actualiza el porcentaje de fatiga2 en un resultado existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE resultados SET porcentaje_fatiga2 = %s WHERE idResult = %s",
        (porcentaje_fatiga2, idResult)
    )
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_capacidad_perceptiva(idResult, capacidad_perceptiva):
    """Actualiza la capacidad perceptiva en un resultado existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE resultados SET capacidad_perceptiva = %s WHERE idResult = %s",
        (capacidad_perceptiva, idResult)
    )
    conn.commit()
    cursor.close()
    conn.close()

def actualizar_resultado_final(idResult, resultado_final):
    """Actualiza el resultado final en un resultado existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE resultados SET resultado_final = %s WHERE idResult = %s",
        (resultado_final, idResult)
    )
    conn.commit()
    cursor.close()
    conn.close()

def obtener_resultados(idUser):
    """Obtiene los resultados de un usuario específico."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resultados WHERE idUser = %s", (idUser,))
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados

def obtener_nombre_usuario(idUser):
    """Obtiene el nombre del usuario a partir de su idUser."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT usuario FROM users WHERE idUser = %s", (idUser,))
    nombre_usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if nombre_usuario:
        return nombre_usuario[0]
    return None  # Retorna None si no se encuentra el usuario

