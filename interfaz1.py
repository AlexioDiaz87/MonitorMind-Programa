import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import random
import time
from tkinter import messagebox
import os
import resultados1

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("MonitorMind")

# Configurar la ventana para que se maximice automáticamente
ventana.state("zoomed")  # Solo en Windows
ventana.configure(bg="#000000")  # Color de fondo

# Obtener el tamaño de la ventana
ventana.update_idletasks()
ancho_ventana = ventana.winfo_width()
alto_ventana = ventana.winfo_height()

# Cargar imágenes
try:
    # Obtén la ruta del directorio donde se encuentra el archivo .py
    directorio_actual = os.path.dirname(__file__)

    # Construye las rutas de las imágenes de forma relativa al directorio actual
    ruta_imagen = os.path.join(directorio_actual, "cerebro.png")
    ruta_icono_inicio = os.path.join(directorio_actual, "camara.png")
    ruta_icono_test = os.path.join(directorio_actual, "test.png")
    ruta_icono_resultados = os.path.join(directorio_actual, "resultados.png")

    # Verifica si los archivos existen
    if not all(os.path.exists(ruta) for ruta in [ruta_imagen, ruta_icono_inicio, ruta_icono_test, ruta_icono_resultados]):
        print(f"Error: No se encontraron todos los archivos necesarios en las rutas especificadas.")
    else:
        # Abre las imágenes y las redimensiona
        imagen = Image.open(ruta_imagen).resize((300, 300), Image.Resampling.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)

        icono_inicio = Image.open(ruta_icono_inicio).resize((60, 60), Image.Resampling.LANCZOS)
        icono_inicio_tk = ImageTk.PhotoImage(icono_inicio)

        icono_test = Image.open(ruta_icono_test).resize((60, 60), Image.Resampling.LANCZOS)
        icono_test_tk = ImageTk.PhotoImage(icono_test)

        icono_resultados = Image.open(ruta_icono_resultados).resize((60, 60), Image.Resampling.LANCZOS)
        icono_resultados_tk = ImageTk.PhotoImage(icono_resultados)

except Exception as e:
    print(f"Error al cargar imágenes: {e}")



# Título estilizado
titulo = tk.Label(
    ventana,
    text="MonitorMind",
    font=("Hello Valentica", 60, "bold"),
    fg="white",
    bg="#000000"
)
titulo.place(relx=0.5, rely=0.7, anchor="center")  # Posicionar el texto más arriba o abajo según necesites

# Crear la etiqueta para la imagen en la primera interfaz
label_imagen = tk.Label(ventana, image=imagen_tk, bg="#000000")
label_imagen.place(relx=0.5, rely=0.4, anchor="center")  # Posicionar la imagen en la primera interfaz

# Crear el canvas para la barra de carga
canvas = tk.Canvas(ventana, width=400, height=30, bg="#000000", bd=0, highlightthickness=0)
canvas.place(relx=0.5, rely=0.9, anchor="center")

# Crear el rectángulo que representará la barra de carga
barra_carga_rect = canvas.create_rectangle(0, 0, 0, 30, fill="#D8A0FF")  # Color lila

# Función para simular el progreso de la barra de carga
def cargar():
    # Simulamos la carga de elementos para la nueva interfaz
    total_steps = 100  # Definimos el número de pasos para simular la carga
    for i in range(total_steps + 1):
        time.sleep(0.05)  # Simula el tiempo de carga para cada paso
        canvas.coords(barra_carga_rect, 0, 0, (i * 4), 30)  # Ajustamos el progreso de la barra
        ventana.update_idletasks()  # Actualiza la interfaz gráfica
        
    # Cuando la barra llega al 100%, reemplaza la interfaz con la segunda
    mostrar_segunda_interfaz()

# Función para reemplazar la interfaz de carga con la segunda interfaz
def mostrar_segunda_interfaz():
    # Ocultar la barra de carga, el título y la imagen
    canvas.place_forget()
    titulo.place_forget()
    label_imagen.place_forget()  # Ocultar la imagen del cerebro

    # Marco izquierdo
    frame_izquierdo = tk.Frame(ventana, bg="#000000")
    frame_izquierdo.grid(row=0, column=0, sticky="nsew", padx=80, pady=30)

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)
    ventana.grid_columnconfigure(1, weight=1)

    # Texto superior
    bienvenida_arriba = tk.Label(
        frame_izquierdo,
        text="¡Bienvenidos!",
        font=("Hello Valentica", 60, "bold"),
        fg="white",
        bg="#000000"
    )
    bienvenida_arriba.pack(pady=20)
    
   
    # Logo
    if imagen_tk:
        logo = tk.Label(frame_izquierdo, image=imagen_tk, bg="#000000")
        logo.pack(pady=30)

    # Texto inferior
    bienvenida_abajo = tk.Label(
        frame_izquierdo,
        text="MonitorMind",
        font=("Hello Valentica", 60, "bold"),
        fg="white",
        bg="#000000"
    )
    bienvenida_abajo.pack(pady=20)

    # Marco derecho para los botones
    frame_derecho = tk.Frame(ventana, bg="#000000")
    frame_derecho.grid(row=0, column=1, sticky="nsew", padx=50, pady=120)  # Aumentar pady para bajar los botones

    # Botón Inicio
    def abrir_inicio():
        try:
            # Obtén la ruta del directorio donde se encuentra el archivo .py
            directorio_actual = os.path.dirname(__file__)

            # Construye la ruta del archivo seleccionarActividad.py
            ruta_actividad = os.path.join(directorio_actual, "seleccionarActividad.py")

            # Verifica si el archivo existe
            if not os.path.exists(ruta_actividad):
                messagebox.showerror("Error", f"No se encontró el archivo 'seleccionarActividad.py' en la ruta: {ruta_actividad}")
                return

            # Ejecuta el archivo seleccionarActividad.py
            subprocess.run(["python", ruta_actividad], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo iniciar la actividad: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    # Botón Inicio
    boton_inicio = tk.Button(
        frame_derecho,
        text="  Inicio",
        font=("Milky Vintage", 24),
        image=icono_inicio_tk,
        compound="left",
        bg="#D8A0FF",
        fg="black",
        width=250,
        height=80,
        command=abrir_inicio
    )
    boton_inicio.pack(pady=35)
    

    # Botón Test
    def abrir_test_tpr():
        def iniciar_test():
            nueva_ventana = tk.Toplevel(ventana)
            nueva_ventana.title("Test Toulouse-Piéron")
            nueva_ventana.state("zoomed")
            nueva_ventana.configure(bg="#FADADD")

            # Crear un Canvas para contener los elementos y permitir el desplazamiento
            canvas_ventana = tk.Canvas(nueva_ventana, bg="#FADADD")
            canvas_ventana.pack(side="left", fill="both", expand=True)

            # Agregar un Scrollbar vertical
            scrollbar = tk.Scrollbar(nueva_ventana, orient="vertical", command=canvas_ventana.yview)
            scrollbar.pack(side="right", fill="y")

            # Configurar el Canvas para usar el Scrollbar
            canvas_ventana.configure(yscrollcommand=scrollbar.set)

            # Crear un Frame dentro del Canvas para contener los elementos
            frame_contenido = tk.Frame(canvas_ventana, bg="#FADADD")
            canvas_ventana.create_window((0, 0), window=frame_contenido, anchor="nw")

            # Variables para resultados del test
            inicio_tiempo = time.time()
            tiempo_restante = tk.IntVar(value=180)  # Tiempo de 1 minuto
            aciertos = tk.IntVar(value=0)
            errores = tk.IntVar(value=0)

            # Modelos de ejemplo
            modelos = [
                {"figura": "⬜-", "color": "blue", "correcto": True},
                {"figura": "-⬜", "color": "blue", "correcto": True}
            ]

            # Cabecera con los modelos y el cronómetro
            frame_modelos = tk.Frame(frame_contenido, bg="#FADADD")
            frame_modelos.pack(pady=10)

            tk.Label(
                frame_modelos,
                text="Modelo 1:",
                font=("Arial", 16),
                fg="black",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_modelos,
                text=modelos[0]["figura"],
                font=("Arial", 24),
                fg=modelos[0]["color"],
                bg="#FADADD"
            ).pack(side="left", padx=20)

            tk.Label(
                frame_modelos,
                text="Modelo 2:",
                font=("Arial", 16),
                fg="black",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_modelos,
                text=modelos[1]["figura"],
                font=("Arial", 24),
                fg=modelos[1]["color"],
                bg="#FADADD"
            ).pack(side="left", padx=20)

            cronometro_label = tk.Label(
                frame_modelos,
                textvariable=tiempo_restante,
                font=("Arial", 24),
                fg="red",
                bg="#FADADD"
            )
            cronometro_label.pack(side="right", padx=20)

            # Función para manejar el cronómetro
            def actualizar_cronometro():
                tiempo = tiempo_restante.get()
                if tiempo > 0:
                    tiempo_restante.set(tiempo - 1)
                    nueva_ventana.after(1000, actualizar_cronometro)
                else:
                    finalizar_test()

            actualizar_cronometro()

            # Función para manejar clics en patrones
            def seleccionar_patron(event):
                item = canvas.find_withtag("current")
                if not item:
                    return

                tags = canvas.gettags(item)
                figura_text = canvas.itemcget(item, "text")

                if figura_text in [modelo["figura"] for modelo in modelos if modelo["correcto"]]:
                    aciertos.set(aciertos.get() + 1)
                    canvas.itemconfig(item, fill="green")
                else:
                    errores.set(errores.get() + 1)
                    canvas.itemconfig(item, fill="red")

            # Generar matriz de patrones
            canvas = tk.Canvas(frame_contenido, width=800, height=600, bg="#FADADD")
            canvas.pack(pady=20)
            canvas.bind("<Button-1>", seleccionar_patron)

            filas, columnas = 15, 20
            figuras = ["⬜-", "-⬜", "⬜\\", "⬜"]
            colores = ["blue", "blue", "blue", "blue"]

            for i in range(filas):
                for j in range(columnas):
                    x1, y1 = 10 + j * 40, 10 + i * 40
                    x2, y2 = x1 + 30, y1 + 30

                    indice = random.randint(0, len(figuras) - 1)
                    figura = figuras[indice]
                    color = "blue"
                    rect = canvas.create_rectangle(x1, y1, x2, y2, fill="#FADADD", outline="black")

                    canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=figura,
                        font=("Arial", 12),
                        fill=color,
                        tags=("figura", "correcto" if figura in ["⬜-", "-⬜"] else "")
                    )

            # Mostrar resultados dinámicos
            frame_resultados = tk.Frame(frame_contenido, bg="#FADADD")
            frame_resultados.pack(pady=10)

            tk.Label(
                frame_resultados,
                text="Aciertos:",
                font=("Arial", 14),
                fg="green",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                textvariable=aciertos,
                font=("Arial", 14),
                fg="green",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                text="Errores:",
                font=("Arial", 14),
                fg="red",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                textvariable=errores,
                font=("Arial", 14),
                fg="red",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            # Botón para finalizar el test
            def finalizar_test():
                tiempo_total = time.time() - inicio_tiempo
                aciertos_total = aciertos.get()
                errores_total = errores.get()
                total_patrones = filas * columnas  # Total de patrones en la matriz
                omisiones_total = total_patrones - (aciertos_total + errores_total)

                # Calcular el IGAP usando la función de resultados.py
                igap = resultados1.calcular_igap(aciertos_total, errores_total, omisiones_total)

                # Guardar los resultados en un archivo usando la función de resultados.py
                resultados1.guardar_resultados(aciertos_total, errores_total, omisiones_total, igap)

                # Calcular el porcentaje de capacidad perceptiva
                capacidad_perceptiva = resultados1.calcular_capacidad_perceptiva(aciertos_total, errores_total, omisiones_total)


                # Mostrar los resultados en un messagebox
                resultados_finales = (
                    f"Tiempo total: {tiempo_total:.2f} segundos\n"
                    f"Aciertos: {aciertos_total}\n"
                    f"Errores: {errores_total}\n"
                    f"Omisiones: {omisiones_total}\n"
                    f"IGAP: {igap}"
                    f"Capacidad Perceptiva: {capacidad_perceptiva}%\n"
                )
                messagebox.showinfo("Resultados del Test", resultados_finales)
                nueva_ventana.destroy()

            boton_finalizar = tk.Button(
                frame_contenido,
                text="Finalizar Test",
                font=("Arial", 14),
                bg="#D8A0FF",
                fg="black",
                command=finalizar_test
            )
            boton_finalizar.pack(pady=20)

            # Actualizar el scrollregion del Canvas después de agregar todos los elementos
            frame_contenido.update_idletasks()
            canvas_ventana.configure(scrollregion=canvas_ventana.bbox("all"))

        # Llamar a la función iniciar_test para que se ejecute al hacer clic en el botón
        iniciar_test()

    boton_test = tk.Button(
    frame_derecho,
    text="  Test",
    font=("Milky Vintage", 24),
    image=icono_test_tk,
    compound="left",
    bg="#D8A0FF",
    fg="black",
    width=250,
    height=80,
    command=abrir_test_tpr
    )
    boton_test.pack(pady=35)

    

    # Botón Resultados
    def abrir_resultados():
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(ventana)
        ventana_resultados.title("Resultados")
        ventana_resultados.state("zoomed")
        ventana_resultados.configure(bg="#000000")

        # Título de la ventana de resultados
        titulo_resultados = tk.Label(
            ventana_resultados,
            text="Resultados",
            font=("Hello Valentica", 60, "bold"),
            fg="white",
            bg="#000000"
        )
        titulo_resultados.pack(pady=20)

        # Leer los resultados guardados en el archivo
        try:
            with open("resultados.txt", "r") as archivo:
                resultados_texto = archivo.read()
        except FileNotFoundError:
            resultados_texto = "No hay resultados disponibles."

        # Mostrar los resultados en un label dentro de la ventana
        label_resultados = tk.Label(
            ventana_resultados,
            text=resultados_texto,
            font=("Arial", 24),
            fg="white",
            bg="#000000",
            justify="left"
        )
        label_resultados.pack(pady=50)

        # Aquí puedes agregar más contenido, como gráficos, tablas, etc.
        # Por ejemplo, un label con un mensaje de ejemplo:
        mensaje_resultados = tk.Label(
            ventana_resultados,
            text="Aquí se mostrarán los resultados de las pruebas realizadas.",
            font=("Arial", 24),
            fg="white",
            bg="#000000"
        )
        mensaje_resultados.pack(pady=50)

        # Función para cerrar la ventana y borrar el archivo de resultados
        def cerrar_ventana():
            ventana_resultados.destroy()  # Cierra la ventana
            try:
                os.remove("resultados.txt")  # Elimina el archivo de resultados
            except FileNotFoundError:
                pass  # Si el archivo no existe, no hacer nada

        # Botón para cerrar la ventana de resultados
        boton_cerrar = tk.Button(
            ventana_resultados,
            text="Cerrar",
            font=("Arial", 18),
            bg="#D8A0FF",
            fg="black",
            command=ventana_resultados.destroy
        )
        boton_cerrar.pack(pady=20)

    # Agregar el botón de Resultados en la interfaz
    boton_resultados = tk.Button(
        frame_derecho,
        text="  Resultados",
        font=("Milky Vintage", 24),
        image=icono_resultados_tk,
        compound="left",
        bg="#D8A0FF",
        fg="black",
        width=250,
        height=80,
        command=abrir_resultados
    )
    boton_resultados.pack(pady=35)

    # Botón para regresar a la ventana principal
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

# Iniciar la carga inmediatamente
ventana.after(500, cargar)  # Llamar a cargar después de 500 ms

# Ejecutar la ventana principal
ventana.mainloop()