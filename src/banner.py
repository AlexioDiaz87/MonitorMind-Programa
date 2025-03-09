import os
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# Obtén la ruta del directorio donde se encuentra el script
directorio_actual = os.path.dirname(__file__)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("MonitorMind")
ventana.state("zoomed")
ventana.configure(bg="#add8e6")

# Sección del título
frame_titulo = tk.Frame(ventana, bg="#add8e6")
frame_titulo.place(relx=0.5, rely=0.25, anchor="center")

titulo = tk.Label(
    frame_titulo,
    text="MonitorMind",
    font=("Hello Valentica", 80, "bold"),
    fg="black",
    bg="#add8e6",
)
titulo.pack()

subtitulo = tk.Label(
    frame_titulo,
    text="Un Viaje hacia la Excelencia Mental",
    font=("Milky Vintage", 30),
    fg="black",
    bg="#add8e6",
)
subtitulo.pack()

# Sección de la imagen del cerebro
frame_cerebro = tk.Frame(ventana, bg="#add8e6")
frame_cerebro.place(relx=0.5, rely=0.6, anchor="center")

try:
    ruta_cerebro = os.path.join(directorio_actual, "../assets/images/cerebro.png")
    cerebro_imagen = Image.open(ruta_cerebro).resize((250, 250), Image.Resampling.LANCZOS)
    cerebro_tk = ImageTk.PhotoImage(cerebro_imagen)
    cerebro_label = tk.Label(frame_cerebro, image=cerebro_tk, bg="#add8e6")
    cerebro_label.pack()
except FileNotFoundError as e:
    print(f"Error al cargar la imagen del cerebro: {e}")

def abrir_sobre_nosotros():
    ventana_sobre = tk.Toplevel(ventana)
    ventana_sobre.title("Sobre Nosotros")
    ventana_sobre.geometry("900x500")
    ventana_sobre.configure(bg="#add8e6")

    try:
        ruta_cerebro = os.path.join(directorio_actual, "../assets/images/cerebro.png")
        cerebro_image = Image.open(ruta_cerebro).resize((100, 100), Image.Resampling.LANCZOS)
        cerebro_photo = ImageTk.PhotoImage(cerebro_image)

        # Etiqueta para la imagen
        imagen_label = tk.Label(ventana_sobre, image=cerebro_photo, bg="#add8e6")
        imagen_label.image = cerebro_photo  # Mantener una referencia a la imagen
        imagen_label.place(relx=0.1, rely=0.2, anchor="center")
    except FileNotFoundError as e:
        print(f"Error al cargar la imagen del cerebro en 'Sobre Nosotros': {e}")

    # Título
    titulo_sobre = tk.Label(
        ventana_sobre,
        text="MonitorMind",
        font=("Hello Valentica", 60, "bold"),
        fg="black",
        bg="#add8e6",
    )
    titulo_sobre.place(relx=0.5, rely=0.2, anchor="center")

    # Descripción
    descripcion = tk.Label(
        ventana_sobre,
        text=(
            "MonitorMind es una aplicación innovadora creada en la Universidad de las Fuerzas Armadas.\n"
            "Su objetivo principal es ayudar a detectar señales de fatiga y estrés mental utilizando\n"
            "tecnología avanzada. Diseñada para mejorar el bienestar mental, MonitorMind se\n"
            "basa en investigaciones científicas para ofrecer una experiencia única a sus usuarios.\n\n"
            
        ),
        font=("Milky Vintage", 18),
        fg="#000000",
        bg="#add8e6",
        justify="center",  # Alineación del texto
        wraplength=800,    # Longitud máxima de línea
    )
    descripcion.place(relx=0.5, rely=0.5, anchor="center")

    # Botón para cerrar la ventana
    boton_cerrar_sobre = tk.Button(
        ventana_sobre,
        text="Cerrar",
        font=("Milky Vintage", 18, "bold"),
        bg="#66AEF0",
        fg="#000000",
        command=ventana_sobre.destroy,
    )
    boton_cerrar_sobre.place(relx=0.5, rely=0.8, anchor="center")

# Función para continuar
def continuar():
    ventana.destroy()
    try:
        ruta_interfaz1 = os.path.join(directorio_actual, "login.py")
        subprocess.run(["python", ruta_interfaz1])
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo 'login.py': {e}")
    except Exception as e:
        print(f"Error al ejecutar 'login.py': {e}")

# Sección de botones
frame_botones = tk.Frame(ventana, bg="#add8e6")
frame_botones.place(relx=0.5, rely=0.8, anchor="center")

boton_continuar = tk.Button(
    frame_botones,
    text="Comenzar",
    font=("Milky Vintage", 20, "bold"),
    fg="black",
    bg="#add8e6",
    highlightbackground="#FFD700",
    highlightthickness=2,
    bd=0,
    command=continuar,
    width=15,
    height=1,
)
boton_continuar.grid(row=0, column=0, padx=20)

boton_sobre_nosotros = tk.Button(
    frame_botones,
    text="Sobre Nosotros",
    font=("Milky Vintage", 20, "bold"),
    fg="black",
    bg="#add8e6",
    highlightbackground="#FFD700",
    highlightthickness=2,
    bd=0,
    command=abrir_sobre_nosotros,
    width=15,
    height=1,
)
boton_sobre_nosotros.grid(row=0, column=1, padx=20)

# Línea negra con redes sociales y @MonitorMind
frame_footer = tk.Frame(ventana, bg="black", height=50)
frame_footer.pack(side="bottom", fill="x")

label_monitor_mind = tk.Label(frame_footer, text="@MonitorMind", fg="white", bg="black", font=("Arial", 16, "bold"))
label_monitor_mind.pack(side="left", padx=20)

frame_redes = tk.Frame(frame_footer, bg="black")
frame_redes.pack(side="top", pady=5)

try:
    # Construye las rutas de las imágenes de redes sociales
    ruta_imagen1 = os.path.join(directorio_actual, "../assets/images/imagen1.png")
    ruta_imagen2 = os.path.join(directorio_actual, "../assets/images/imagen2.jpg")
    ruta_imagen3 = os.path.join(directorio_actual, "../assets/images/imagen3.jpg")
    
    # Carga las imágenes
    imagen1 = ImageTk.PhotoImage(Image.open(ruta_imagen1).resize((30, 30), Image.Resampling.LANCZOS))
    imagen2 = ImageTk.PhotoImage(Image.open(ruta_imagen2).resize((30, 30), Image.Resampling.LANCZOS))
    imagen3 = ImageTk.PhotoImage(Image.open(ruta_imagen3).resize((30, 30), Image.Resampling.LANCZOS))
    
    # Muestra las imágenes en la interfaz
    tk.Label(frame_footer, image=imagen1, bg="black").pack(side="right", padx=10)
    tk.Label(frame_footer, image=imagen2, bg="black").pack(side="right", padx=10)
    tk.Label(frame_footer, image=imagen3, bg="black").pack(side="right", padx=10)
except FileNotFoundError as e:
    print(f"Error al cargar las imágenes de redes sociales: {e}")

ventana.mainloop()