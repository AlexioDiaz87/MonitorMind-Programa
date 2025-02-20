import tkinter as tk
import sqlite3
import hashlib
import subprocess
from PIL import Image, ImageTk

# Configurar base de datos
def inicializar_bd():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    
    # Crear la tabla de usuarios si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            actividad1 TEXT,
            actividad2 TEXT,
            test TEXT,
            resultadoGeneral TEXT
        )
    """)
    conn.commit()
    conn.close()

# Función para hashear contraseñas
def hashear_contrasena(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

# Función para verificar credenciales
def verificar_credenciales(usuario, contrasena):
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT contrasena FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado is None:
        return False
    return resultado[0] == hashear_contrasena(contrasena)
# Función para ventanas emergentes de ADVERTENCIA

def mostrar_advertencia():
    # Crear una nueva ventana (Toplevel)
    ventana = tk.Toplevel()
    ventana.title("Registro")
    ventana.geometry("300x200+{}+{}".format(
        (ventana.winfo_screenwidth() - 300) // 2,  # Centrado en la pantalla
        (ventana.winfo_screenheight() - 200) // 2
    ))
    ventana.configure(bg="#D8A0FF")  # Fondo lila
    
    # Título "MONITORMIND"
    titulo = tk.Label(
        ventana, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"  # Fondo lila
    )
    titulo.pack(pady=0)


    # Etiqueta con el mensaje de advertencia
    label = tk.Label(
        ventana, 
        text="Todos los campos son obligatorios.", 
        font=("Milky Vintage", 18), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"   # Fondo lila
    )
    label.pack(pady=20)

    # Botón personalizado con estilo negro y letras blancas
    boton = tk.Button(
        ventana, 
        text="Aceptar", 
        command=ventana.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF",  # Fondo negro
        fg="black",  # Texto blanco
        width=15,
        height=1,
        relief="flat"  # Sin bordes
    )
    # Centrar el botón usando 'place'
    boton.place(relx=0.5, rely=0.8, anchor="center")  # Colocar en el centro
    
def advertencia_registro():
    # Crear una nueva ventana (Toplevel)
    ventana = tk.Toplevel()
    ventana.title("Registro")
    ventana.geometry("300x200+{}+{}".format(
        (ventana.winfo_screenwidth() - 300) // 2,  # Centrado en la pantalla
        (ventana.winfo_screenheight() - 200) // 2
    ))
    ventana.configure(bg="#D8A0FF")  # Fondo lila
    
    # Título "MONITORMIND"
    titulo = tk.Label(
        ventana, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"  # Fondo lila
    )
    titulo.pack(pady=0)


    # Etiqueta con el mensaje de advertencia
    label = tk.Label(
        ventana, 
        text="Cuenta creada exitosamente.", 
        font=("Milky Vintage", 18), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"   # Fondo lila
    )
    label.pack(pady=20)

    # Botón personalizado con estilo negro y letras blancas
    boton = tk.Button(
        ventana, 
        text="Aceptar", 
        command=ventana.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF",  # Fondo negro
        fg="black",  # Texto blanco
        width=15,
        height=1,
        relief="flat"  # Sin bordes
    )
    # Centrar el botón usando 'place'
    boton.place(relx=0.5, rely=0.8, anchor="center")  # Colocar en el centro

def advertencia_registro_error():
    # Crear una nueva ventana (Toplevel)
    ventana = tk.Toplevel()
    ventana.title("Registro - Error")
    ventana.geometry("300x200+{}+{}".format(
        (ventana.winfo_screenwidth() - 300) // 2,  # Centrado en la pantalla
        (ventana.winfo_screenheight() - 200) // 2
    ))
    ventana.configure(bg="#D8A0FF")  # Fondo lila
    
    # Título "MONITORMIND"
    titulo = tk.Label(
        ventana, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"  # Fondo lila
    )
    titulo.pack(pady=0)


    # Etiqueta con el mensaje de advertencia
    label = tk.Label(
        ventana, 
        text="El usuario ya existe.", 
        font=("Milky Vintage", 18), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"   # Fondo lila
    )
    label.pack(pady=20)

    # Botón personalizado con estilo negro y letras blancas
    boton = tk.Button(
        ventana, 
        text="Aceptar", 
        command=ventana.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF",  # Fondo negro
        fg="black",  # Texto blanco
        width=15,
        height=1,
        relief="flat"  # Sin bordes
    )
    # Centrar el botón usando 'place'
    boton.place(relx=0.5, rely=0.8, anchor="center")  # Colocar en el centro

def advertencia_sesion():
    # Crear una nueva ventana (Toplevel)
    ventana = tk.Toplevel()
    ventana.title("Inicio de sesión")
    ventana.geometry("300x200+{}+{}".format(
        (ventana.winfo_screenwidth() - 300) // 2,  # Centrado en la pantalla
        (ventana.winfo_screenheight() - 200) // 2
    ))
    ventana.configure(bg="#D8A0FF")  # Fondo lila
    
    # Título "MONITORMIND"
    titulo = tk.Label(
        ventana, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"  # Fondo lila
    )
    titulo.pack(pady=0)


    # Etiqueta con el mensaje de advertencia
    label = tk.Label(
        ventana, 
        text="Acceso concedido.", 
        font=("Milky Vintage", 18), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"   # Fondo lila
    )
    label.pack(pady=20)

    # Botón personalizado con estilo negro y letras blancas
    boton = tk.Button(
        ventana, 
        text="Aceptar", 
        command=ventana.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF",  # Fondo negro
        fg="black",  # Texto blanco
        width=15,
        height=1,
        relief="flat"  # Sin bordes
    )
    # Centrar el botón usando 'place'
    boton.place(relx=0.5, rely=0.8, anchor="center")  # Colocar en el centro

def advertencia_sesion_error():
    # Crear una nueva ventana (Toplevel)
    ventana = tk.Toplevel()
    ventana.title("Inicio de sesión - Error")
    ventana.geometry("300x200+{}+{}".format(
        (ventana.winfo_screenwidth() - 300) // 2,  # Centrado en la pantalla
        (ventana.winfo_screenheight() - 200) // 2
    ))
    ventana.configure(bg="#D8A0FF")  # Fondo lila
    
    # Título "MONITORMIND"
    titulo = tk.Label(
        ventana, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"  # Fondo lila
    )
    titulo.pack(pady=0)


    # Etiqueta con el mensaje de advertencia
    label = tk.Label(
        ventana, 
        text="Usuario o contraseña incorrectos.", 
        font=("Milky Vintage", 18), 
        fg="black",  # Texto en negro
        bg="#D8A0FF"   # Fondo lila
    )
    label.pack(pady=20)

    # Botón personalizado con estilo negro y letras blancas
    boton = tk.Button(
        ventana, 
        text="Aceptar", 
        command=ventana.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF",  # Fondo negro
        fg="black",  # Texto blanco
        width=15,
        height=1,
        relief="flat"  # Sin bordes
    )
    # Centrar el botón usando 'place'
    boton.place(relx=0.5, rely=0.8, anchor="center")  # Colocar en el centro

# Función para registrar un nuevo usuario
def registrar_usuario():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if not usuario or not contrasena:
        mostrar_advertencia()
        return
    
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)", (usuario, hashear_contrasena(contrasena)))
        conn.commit()
        advertencia_registro()
    except sqlite3.IntegrityError:
        advertencia_registro_error()
    finally:
        conn.close()

def iniciar_sesion():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if verificar_credenciales(usuario, contrasena):
        advertencia_sesion ()
        ventana.destroy()
        subprocess.run(["python", "interfaz1.py"])  # Asegúrate de que el nombre del archivo principal sea correcto
    else:
        advertencia_sesion_error()
        


# Inicializar BD
inicializar_bd()

# Crear ventana de login
ventana = tk.Tk()
ventana.title("MonitorMind Login")
ventana.state("zoomed")  # Maximiza la ventana
ventana.configure(bg="black")

# Añadir un logo a la izquierda
logo = Image.open("cerebro.png")  
logo = logo.resize((150, 150), Image.Resampling.LANCZOS)
logo_img = ImageTk.PhotoImage(logo)

logo_label = tk.Label(ventana, image=logo_img, bg="#000000")
logo_label.place(x=365, y=60)  # Coloca el logo a la izquierda y un poco abajo

# Título estilizado
titulo = tk.Label(
    ventana,
    text="MonitorMind",
    font=("Hello Valentica", 70, "bold"),
    fg="white",
    bg="#000000"
)
titulo.place(relx=0.55, rely=0.2, anchor="center")  # Ajusta el `rely` para moverlo un poco más abajo

# Campos de usuario y contraseña
usuario_label = tk.Label(ventana, text="Usuario:", fg="white", bg="#000000", font=("Milky Vintage", 24))
usuario_label.place(x=350, y=300)  # Centrado y un poco a la izquierda
entry_usuario = tk.Entry(ventana, font=("Arial", 16), width=40)  # Aumentado tamaño de cuadros
entry_usuario.place(x=550, y=318, anchor="w")

contrasena_label = tk.Label(ventana, text="Contraseña:", fg="white", bg="#000000", font=("Milky Vintage", 24))
contrasena_label.place(x=350, y=400)  # Centrado y un poco a la izquierda
entry_contrasena = tk.Entry(ventana, font=("Arial", 16), show="*", width=40)  # Aumentado tamaño de cuadros
entry_contrasena.place(x=550, y=410)

# Botones de acción con estilo similar a la imagen
iniciar_button = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion, font=("Milky Vintage", 16), bg="#D8A0FF", fg="black", width=20, relief="flat", height=2)
iniciar_button.place(x=445, y=550)

registrarse_button = tk.Button(ventana, text="Registrarse", command=registrar_usuario, font=("Milky Vintage", 16), bg="#D8A0FF", fg="black", width=20, relief="flat", height=2)
registrarse_button.place(x=740, y=550)

# Mostrar la ventana
ventana.mainloop()
