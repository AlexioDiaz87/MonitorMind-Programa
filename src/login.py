# login.py

import tkinter as tk
import subprocess
from PIL import Image, ImageTk
from db import inicializar_bd, verificar_credenciales, registrar_usuario_db, guardar_sesion

# Función genérica para mostrar ventanas emergentes
def show_popup(window_title, message):
    ventana_popup = tk.Toplevel()
    ventana_popup.title(window_title)
    ventana_popup.geometry("300x200+{}+{}".format(
        (ventana_popup.winfo_screenwidth() - 300) // 2,
        (ventana_popup.winfo_screenheight() - 200) // 2
    ))
    ventana_popup.configure(bg="#D8A0FF")
    
    titulo_label = tk.Label(
        ventana_popup, 
        text="MonitorMind", 
        font=("Hello Valentica", 30, "bold"), 
        fg="black", 
        bg="#D8A0FF"
    )
    titulo_label.pack(pady=0)
    
    msg_label = tk.Label(
        ventana_popup, 
        text=message, 
        font=("Milky Vintage", 18), 
        fg="black", 
        bg="#D8A0FF"
    )
    msg_label.pack(pady=20)
    
    boton = tk.Button(
        ventana_popup, 
        text="Aceptar", 
        command=ventana_popup.destroy,
        font=("Milky Vintage", 15),
        bg="#B547FF", 
        fg="black", 
        width=15,
        height=1,
        relief="flat"
    )
    boton.place(relx=0.5, rely=0.8, anchor="center")

# Funciones de mensajes específicos
def mostrar_advertencia():
    show_popup("Registro", "Todos los campos son obligatorios.")

def advertencia_registro():
    show_popup("Registro", "Cuenta creada exitosamente.")

def advertencia_registro_error():
    show_popup("Registro - Error", "El usuario ya existe.")

def advertencia_sesion():
    show_popup("Inicio de sesión", "Acceso concedido.")

def advertencia_sesion_error():
    show_popup("Inicio de sesión - Error", "Usuario o contraseña incorrectos.")

# Función para registrar un nuevo usuario
def registrar_usuario():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if not usuario or not contrasena:
        mostrar_advertencia()
        return
    
    if registrar_usuario_db(usuario, contrasena):
        advertencia_registro()
    else:
        advertencia_registro_error()

idUser_actual = None  # Variable global para almacenar el idUser del usuario autenticado

def iniciar_sesion():
    global idUser_actual
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    idUser = verificar_credenciales(usuario, contrasena)
    
    if idUser is not None:
        idUser_actual = idUser  # Guarda el idUser globalmente
        guardar_sesion(idUser_actual)  # ✅ Guarda la sesión para que se recuerde en otras ventanas
        
        advertencia_sesion()
        ventana.destroy()
        subprocess.run(["python", "interfaz1.py"])
    else:
        advertencia_sesion_error()



# Inicializar la base de datos
inicializar_bd()

# Crear ventana de login
ventana = tk.Tk()
ventana.title("MonitorMind Login")
ventana.state("zoomed")
ventana.configure(bg="black")

# Añadir un logo (se intenta cargar desde ../assets/images/cerebro.png)
try:
    logo = Image.open("../assets/images/cerebro.png")
    logo = logo.resize((150, 150), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(ventana, image=logo_img, bg="#000000")
    logo_label.place(x=365, y=60)
except Exception as e:
    print("Error al cargar el logo:", e)

# Título principal
titulo = tk.Label(
    ventana,
    text="MonitorMind",
    font=("Hello Valentica", 70, "bold"),
    fg="white",
    bg="#000000"
)
titulo.place(relx=0.55, rely=0.2, anchor="center")

# Campos de usuario y contraseña
usuario_label = tk.Label(
    ventana, 
    text="Usuario:", 
    fg="white", 
    bg="#000000", 
    font=("Milky Vintage", 24)
)
usuario_label.place(x=350, y=300)
entry_usuario = tk.Entry(ventana, font=("Arial", 16), width=40)
entry_usuario.place(x=550, y=318, anchor="w")

contrasena_label = tk.Label(
    ventana, 
    text="Contraseña:", 
    fg="white", 
    bg="#000000", 
    font=("Milky Vintage", 24)
)
contrasena_label.place(x=350, y=400)
entry_contrasena = tk.Entry(ventana, font=("Arial", 16), show="*", width=40)
entry_contrasena.place(x=550, y=410)

# Botones de acción
iniciar_button = tk.Button(
    ventana, 
    text="Iniciar Sesión", 
    command=iniciar_sesion, 
    font=("Milky Vintage", 16), 
    bg="#D8A0FF", 
    fg="black", 
    width=20, 
    relief="flat", 
    height=2
)
iniciar_button.place(x=445, y=550)

registrarse_button = tk.Button(
    ventana, 
    text="Registrarse", 
    command=registrar_usuario, 
    font=("Milky Vintage", 16), 
    bg="#D8A0FF", 
    fg="black", 
    width=20, 
    relief="flat", 
    height=2
)
registrarse_button.place(x=740, y=550)

ventana.mainloop()
