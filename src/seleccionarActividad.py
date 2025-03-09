import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from tkinter import messagebox
import sys
from db import guardar_resultado, cargar_sesion

import os

# Cargar la sesión guardada
idUser_sesion = cargar_sesion()

if idUser_sesion is not None:
    idResult = guardar_resultado(idUser_sesion)
else:
    print("No hay usuario en sesión")

    # Asegurar que las actividades usan el usuario en sesión:
def start_actividad_1():
    if idUser_sesion is None:
        messagebox.showerror("Error", "No se pudo identificar al usuario")
        return
    try:
        subprocess.run(["python", "conjunta.py"])  # ✅ Llama a la actividad correctamente
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo 'conjunta.py'.")

class MainMenu:
    def __init__(self, root):  
        self.root = root
        self.root.title("Menú Principal")
        self.root.state("zoomed")  # Pantalla completa
        self.root.configure(bg="black")

        directorio_actual = os.path.dirname(__file__)

        # Encabezado con logo y título
        self.header_frame = tk.Frame(self.root, bg="black")
        self.header_frame.pack(pady=10, fill="x")

        # Logo
        try:
            ruta_logo = os.path.join(directorio_actual, "../assets/images/cerebro.png")
            self.logo_image = Image.open(ruta_logo).resize((140, 140), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: {ruta_logo}")
            return

        # Título
        title_frame = tk.Frame(self.root, bg="black")
        title_frame.pack(pady=20)
        logo_label = tk.Label(title_frame, image=self.logo_photo, bg="black")
        logo_label.pack(side="left", padx=10)
        title_label = tk.Label(
            title_frame, text="MonitorMind", font=("Hello Valentica", 65, "bold"), bg="black", fg="white"
        )
        title_label.pack(side="left")

        # Sección "Seleccionar Actividad" a la izquierda
        subtitle_label = tk.Label(
            self.root,
            text="Seleccionar Actividad:",
            font=("Hello Valentica", 35),
            bg="black",
            fg="#75FFEB"
        )
        subtitle_label.place(relx=0.05, rely=0.33, anchor="w")  # Posición más a la izquierda

        # Contenedor principal para las actividades
        self.activities_frame = tk.Frame(self.root, bg="black")
        self.activities_frame.pack(pady=40, fill="x", expand=True)  # Llenar horizontalmente

        # Actividad 1 (Lectura Atenta)
        self.left_activity_frame = tk.Frame(self.activities_frame, bg="black")
        self.left_activity_frame.pack(side="left", padx=0, expand=True)  # Más a la izquierda

        lectura_label = tk.Label(
            self.left_activity_frame,
            text="Lectura Atenta",
            font=("Milky Vintage", 28),
            bg="black",
            fg="white"
        )
        lectura_label.pack(pady=10)

        try:
            ruta_libros = os.path.join(directorio_actual, "../assets/images/libros.png")
            libros_image = Image.open(ruta_libros).resize((350, 200), Image.Resampling.LANCZOS)
            self.libros_photo = ImageTk.PhotoImage(libros_image)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: libros.png")
            return
        libros_label = tk.Label(self.left_activity_frame, image=self.libros_photo, bg="black")
        libros_label.pack()

        iniciar_lectura_button = tk.Button(
            self.left_activity_frame,
            text="Iniciar",
            font=("Milky Vintage", 20),
            bg="#FF69D4",
            fg="black",
            command=self.start_actividad_1
        )
        iniciar_lectura_button.pack(pady=10)

        

        # Actividad 2
        self.right_activity_frame = tk.Frame(self.activities_frame, bg="black")
        self.right_activity_frame.pack(side="left", padx=0, expand=True)  # Más a la izquierda también

        actividad2_label = tk.Label(
            self.right_activity_frame,
            text="Velocidad de Reacción",
            font=("Milky Vintage", 28),
            bg="black",
            fg="white"
        )
        actividad2_label.pack(pady=10)

        try:
            ruta_actividad2 = os.path.join(directorio_actual, "../assets/images/actividad2.png")
            actividad2_image = Image.open(ruta_actividad2).resize((350, 200), Image.Resampling.LANCZOS)
            self.actividad2_photo = ImageTk.PhotoImage(actividad2_image)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: actividad2.png")
            return
        actividad2_label = tk.Label(self.right_activity_frame, image=self.actividad2_photo, bg="black")
        actividad2_label.pack()

        iniciar_actividad2_button = tk.Button(
            self.right_activity_frame,
            text="Iniciar",
            font=("Milky Vintage", 20),
            bg="#FF69D4",
            fg="black",
            command=self.start_actividad_2
        )
        iniciar_actividad2_button.pack(pady=10)
        
        # Botón Resultados
        self.resultados_button = tk.Button(
            self.root,
            text="Resultados",
            font=("Milky Vintage", 20),
            bg="#DBDBDB",
            fg="black",
            command=self.abrir_resultados
        )
        self.resultados_button.place(relx=0.5, rely=0.95, anchor="center")  # Posiciona el botón en la parte inferior derecha

        # Botón Regresar
        self.regresar_button = tk.Button(
            self.root,
            text="Regresar",
            font=("Milky Vintage", 20),
            bg="#DBDBDB",
            fg="black",
            command=self.regresar
        )
        self.regresar_button.place(relx=0.94, rely=0.95, anchor="center")

    def abrir_resultados(self):
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title("Resultados")
        ventana_resultados.state("zoomed")
        ventana_resultados.configure(bg="black")

        
        # Título de la ventana de resultados
        titulo_resultados = tk.Label(
            ventana_resultados,
            text="Resultados",
            font=("Hello Valentica", 60, "bold"),
            fg="white",
            bg="black"
        )
        titulo_resultados.pack(pady=20)

         # Crear un marco para organizar los resultados en dos columnas (izquierda y derecha)
        frame_contenedor = tk.Frame(ventana_resultados, bg="black")
        frame_contenedor.pack(fill="both", expand=True, padx=50, pady=20)

        # **Marco izquierdo (para la actividad de lectura)**
        frame_izquierdo = tk.Frame(frame_contenedor, bg="black")
        frame_izquierdo.pack(side="left", expand=True, fill="both", padx=50)

        label_izq = tk.Label(
            frame_izquierdo,
            text="Resultados de la Actividad de Lectura",
            font=("Hello Valentica", 28),
            fg="#75FFEB",
            bg="black"
        )
        label_izq.pack(pady=10)

        # Leer los resultados desde `resultados2.txt`
        try:
            with open("resultados2.txt", "r") as archivo:
                resultados_lectura = archivo.read()
        except FileNotFoundError:
            resultados_lectura = "No hay resultados disponibles."

        # Mostrar los resultados en un label dentro de la ventana
        label_resultados_izq = tk.Label(
            frame_izquierdo,
            text=resultados_lectura,
            font=("Milky Vintage", 20),
            fg="white",
            bg="black",
            justify="left"
        )
        label_resultados_izq.pack(pady=10)

        # **Marco derecho (Resultados de la actividad 2 - Figuras geométricas)**
        frame_derecho = tk.Frame(frame_contenedor, bg="black")
        frame_derecho.pack(side="right", expand=True, fill="both", padx=50)

        label_der = tk.Label(
            frame_derecho,
            text="Resultados de la Actividad de Figuras",
            font=("Hello Valentica", 28),
            fg="#75FFEB",
            bg="black"
        )
        label_der.pack(pady=10)

        # Leer los resultados desde `resultados3.txt`
        try:
            with open("resultados3.txt", "r") as archivo:
                resultados_figuras = archivo.read()
        except FileNotFoundError:
            resultados_figuras = "No hay resultados disponibles."

        # Mostrar los resultados de la actividad 2 en la parte derecha
        label_resultados_der = tk.Label(
            frame_derecho,
            text=resultados_figuras,
            font=("Milky Vintage", 20),
            fg="white",
            bg="black",
            justify="left"
        )
        label_resultados_der.pack(pady=10)

        # Función para cerrar la ventana y borrar el archivo de resultados
        def cerrar_ventana():
            ventana_resultados.destroy()  # Cierra la ventana
            try:
                os.remove("resultados2.txt")  # Elimina los resultados de la actividad 1
                os.remove("resultados3.txt")  # Elimina los resultados de la actividad 2
            except FileNotFoundError:
                pass  # Si el archivo no existe, no hacer nada

        # Botón para cerrar la ventana de resultados
        boton_cerrar = tk.Button(
            ventana_resultados,
            text="Cerrar",
            font=("Milky Vintage", 20),
            bg="#FF69D4",
            fg="black",
            command=cerrar_ventana
        )
        boton_cerrar.pack(pady=20)

    def regresar(self):
        self.root.withdraw()  # Ocultar la ventana actual
        try:
            ruta_interfaz1 = os.path.join(os.path.dirname(__file__), "interfaz1.py")
            subprocess.run(["python", ruta_interfaz1])
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'interfaz1.py'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la interfaz: {e}")
        self.root.destroy()  # Cerrar la ventana actual


        
    # Ejecuta el archivo Python para la actividad 1
    def start_actividad_1(self):
        # Crear la ventana de instrucciones
        ventana_instruccion = tk.Toplevel()
        ventana_instruccion.title("Instrucciones - Actividad Lectura")
        ventana_instruccion.geometry("300x320+{}+{}".format(
            (ventana_instruccion.winfo_screenwidth() - 300) // 2,
            (ventana_instruccion.winfo_screenheight() - 200) // 2
        ))
        ventana_instruccion.configure(bg="#D8A0FF")

        # Título "MONITORMIND"
        titulo = tk.Label(
            ventana_instruccion, text="MonitorMind",
            font=("Hello Valentica", 30, "bold"),
            fg="black", bg="#D8A0FF"
        )
        titulo.pack(pady=0)

        # Etiqueta con el mensaje de advertencia
        label = tk.Label(
            ventana_instruccion, 
            text="En esta actividad, se evaluará la detección de fatiga mediante el reconocimiento de bostezos, durante 3 minutos. Se presentará un texto sobre las causas del bostezo, y tu tarea será seleccionar las letras A, E y R cuando aparezcan en el texto.",
            font=("Milky Vintage", 14), 
            fg="black", bg="#D8A0FF",
            wraplength=280  # Ajusta el ancho máximo antes de hacer un salto de línea
        )
        label.pack(pady=20)

        # Botón para cerrar la ventana
        boton = tk.Button(
            ventana_instruccion, text="Aceptar",
            command=ventana_instruccion.destroy,
            font=("Milky Vintage", 15),
            bg="#B547FF", fg="black",
            width=15, height=1, relief="flat"
        )
        boton.place(relx=0.5, rely=0.8, anchor="center")

        # Esperar a que la ventana se cierre antes de ejecutar `conjunta.py`
        ventana_instruccion.wait_window()

        # Ahora ejecuta el archivo Python para la actividad 1
        try:
            ruta_conjunta = os.path.join(os.path.dirname(__file__), "conjunta.py")
            subprocess.run(["python", ruta_conjunta])
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'conjunta.py'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la actividad: {e}")

    # Ejecuta el archivo Python para la actividad 2
    def start_actividad_2(self):

        # Crear la ventana de instrucciones
        ventana_instruccion = tk.Toplevel()
        ventana_instruccion.title("Instrucciones - Actividad Figuras")
        ventana_instruccion.geometry("300x320+{}+{}".format(
            (ventana_instruccion.winfo_screenwidth() - 300) // 2,
            (ventana_instruccion.winfo_screenheight() - 200) // 2
        ))
        ventana_instruccion.configure(bg="#D8A0FF")

        # Título "MONITORMIND"
        titulo = tk.Label(
            ventana_instruccion, text="MonitorMind",
            font=("Hello Valentica", 30, "bold"),
            fg="black", bg="#D8A0FF"
        )
        titulo.pack(pady=0)

        # Etiqueta con el mensaje de advertencia
        label = tk.Label(
            ventana_instruccion, 
            text="En esta actividad, se evaluará la detección de fatiga mediante el reconocimiento de bostezos, durante 2 minutos. El objetivo de esta actividad es medir tu velocidad de reacción al hacer clic en un triángulo que aparece en la pantalla, mientras se muestran otras figuras que no debes tocar.",
            font=("Milky Vintage", 14), 
            fg="black", bg="#D8A0FF",
            wraplength=280  # Ajusta el ancho máximo antes de hacer un salto de línea
        )
        label.pack(pady=20)

        # Botón para cerrar la ventana
        boton = tk.Button(
            ventana_instruccion, text="Aceptar",
            command=ventana_instruccion.destroy,
            font=("Milky Vintage", 15),
            bg="#B547FF", fg="black",
            width=15, height=1, relief="flat"
        )
        boton.place(relx=0.5, rely=0.8, anchor="center")

        # Esperar a que la ventana se cierre antes de ejecutar `conjunta.py`
        ventana_instruccion.wait_window()
        
        # Ejecuta el archivo Python para la actividad 2
        try:
            ruta_actividad2 = os.path.join(os.path.dirname(__file__), "actividad2.py")
            subprocess.run(["python", ruta_actividad2])
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'actividad2.py'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la actividad: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
