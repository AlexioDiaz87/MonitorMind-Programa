import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
import subprocess
import random
import time
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as pdf_canvas
from datetime import datetime
import os
import resultados1
import json

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
        font=("Hello Valentica", 80, "bold"),
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
        font=("Milky Vintage", 30),
        image=icono_inicio_tk,
        compound="left",
        bg="#D8A0FF",
        fg="black",
        width=350,
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

            # Agregar título y mensaje de instrucción
            label_titulo = tk.Label(frame_contenido, text="Test de Toulouse-Piéron", font=("Hello Valentica", 18, "bold"), bg="#FADADD", fg="black")
            label_titulo.pack(pady=10)

            label_instrucciones = tk.Label(frame_contenido, text="Seleccione las figuras que coincidan con los modelos mostrados", font=("Arial", 12), bg="#FADADD", fg="black")
            label_instrucciones.pack(pady=5)

            # Cargar la imagen y redimensionarla
            label_imagen = tk.PhotoImage(file="cerebro.png")  # Asegúrate de que la imagen esté en la misma carpeta
            label_imagen = label_imagen.subsample(25, 25) 

            # Variables para resultados del test
            inicio_tiempo = time.time()
            tiempo_restante = tk.IntVar(value=600)  # Tiempo de 1 minuto
            aciertos = tk.IntVar(value=0)
            errores = tk.IntVar(value=0)

# Agregar mensaje en la misma línea de los modelos
            label_mensaje = tk.Label(frame_contenido, text="⬇ Desplázate hacia abajo para completar el test ⬇",
                         font=("Courier", 12, "bold"), fg="black", bg="#FADADD")

# Posicionarlo a la izquierda usando 'place' para mayor control
            label_mensaje.place(x=10, y=150)  # Ajusta 'y' según la ubicación de los modelos



            # Cargar la imagen de la flecha
            try:
                img_flecha_pil = Image.open("flecha.jpg")
                img_flecha_pil = img_flecha_pil.resize((40, 40))  # Ajusta el tamaño si es necesario
                img_flecha = ImageTk.PhotoImage(img_flecha_pil)
            except Exception as e:
                print("Error cargando la imagen flecha.jpg:", e)
                img_flecha = None

            # Crear un frame para modelos y la flecha
            frame_modelos = tk.Frame(frame_contenido, bg="#FADADD")
            frame_modelos.pack(pady=10)


            # Imagen de flecha entre los modelos
            if img_flecha:
                label_flecha = tk.Label(frame_modelos, image=img_flecha, bg="#FADADD")
                label_flecha.image = img_flecha
                label_flecha.place(x=10, y=10)   # Espacio entre los modelos


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
                font=("Courier", 16),
                fg="black",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_modelos,
                text=modelos[0]["figura"],
                font=("Courier", 24),
                fg=modelos[0]["color"],
                bg="#FADADD"
            ).pack(side="left", padx=20)

            tk.Label(
                frame_modelos,
                text="Modelo 2:",
                font=("Courier", 16),
                fg="black",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_modelos,
                text=modelos[1]["figura"],
                font=("Courier", 24),
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
            canvas = tk.Canvas(frame_contenido, width=1600, height=1600, bg="#FADADD")
            canvas.pack(pady=20)
            canvas.bind("<Button-1>", seleccionar_patron)

            filas, columnas = 40, 40
            figuras = ["⬜-", "-⬜", "⬜\\", "⬜"]
            colores = ["blue", "blue", "blue", "blue"]

            for i in range(filas):
                for j in range(columnas):
                    x1, y1 = 2 + j * 33.7, 2 + i * 40
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
                font=("Courier", 14),
                fg="green",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                textvariable=aciertos,
                font=("Courier", 14),
                fg="green",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                text="Errores:",
                font=("Courier", 14),
                fg="red",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            tk.Label(
                frame_resultados,
                textvariable=errores,
                font=("Courier", 14),
                fg="red",
                bg="#FADADD"
            ).pack(side="left", padx=10)

            
            def guardar_resultados_bd(aciertos, errores, omisiones, igap, capacidad_perceptiva, tiempo_total):
                try:
                    conn = sqlite3.connect("monitor_mind.db")
                    cursor = conn.cursor()

                    # Crear la tabla si no existe
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS resultados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tiempo_total REAL,
                        aciertos INTEGER,
                        errores INTEGER,
                        omisiones INTEGER,
                        igap REAL,
                        capacidad_perceptiva REAL
                    )
                    """)

                    # Insertar un nuevo resultado sin borrar los anteriores
                    cursor.execute("""
                    INSERT INTO resultados (tiempo_total, aciertos, errores, omisiones, igap, capacidad_perceptiva)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (tiempo_total, aciertos, errores, omisiones, igap, capacidad_perceptiva))

                    conn.commit()
                    print("Datos guardados correctamente.")
                
                except sqlite3.Error as e:
                    print(f"Error en la base de datos: {e}")

                finally:
                    conn.close()


            # Botón para finalizar el test
            def finalizar_test():
                font=("Courier", 14),
                tiempo_total = time.time() - inicio_tiempo
                aciertos_total = aciertos.get()
                errores_total = errores.get()
                total_patrones = filas * columnas  # Total de patrones en la matriz
                omisiones_total = total_patrones - (aciertos_total + errores_total)

                # Calcular el IGAP usando la función de resultados.py
                igap = abs( resultados1.calcular_igap(aciertos_total, errores_total, omisiones_total))
                # Calcular el porcentaje de capacidad perceptiva
                capacidad_perceptiva = resultados1.calcular_capacidad_perceptiva(aciertos_total, errores_total, omisiones_total)


                # ✅ Guardar `capacidad_perceptiva` en un archivo JSON
                with open("capacidad_perceptiva.json", "w") as file:
                    json.dump({"capacidad_perceptiva": capacidad_perceptiva}, file)

                # Guardar los resultados en la base de datos
                guardar_resultados_bd(aciertos_total, errores_total, omisiones_total, igap, capacidad_perceptiva, tiempo_total)

                # Mostrar los resultados en un messagebox
                resultados_finales = (
                    f"Tiempo total: {tiempo_total:.2f} segundos\n"
                    f"Aciertos: {aciertos_total}\n"
                    f"Errores: {errores_total}\n"
                    f"Omisiones: {omisiones_total}\n"
                    f"IGAP: {igap} \n"
                    f"Capacidad Perceptiva: {capacidad_perceptiva}%\n"
                )
                
                # Crear la ventana de instrucciones
                ventana_instruccion = tk.Toplevel()
                ventana_instruccion.title("Resultados")
                ventana_instruccion.geometry("300x280+{}+{}".format(
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
                    text=resultados_finales,
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

                
                ventana_instruccion.wait_window()
                
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
    font=("Milky Vintage", 30),
    image=icono_test_tk,
    compound="left",
    bg="#D8A0FF",
    fg="black",
    width=350,
    height=80,
    command=abrir_test_tpr
    )
    boton_test.pack(pady=35)

    def obtener_resultados_bd():
        conn = sqlite3.connect("monitor_mind.db")
        cursor = conn.cursor()
        
        try:
            # Asegúrate de que la tabla tiene una columna 'id' que sea clave primaria autoincremental
            cursor.execute("SELECT * FROM resultados ORDER BY id DESC LIMIT 1")
            resultado = cursor.fetchone()  # Usamos fetchone() en lugar de fetchall()
        except sqlite3.OperationalError as e:
            print(f"Error al obtener resultados: {e}")
            resultado = None
        finally:
            conn.close()

        return resultado

    # Botón Resultados


    def obtener_porcentaje_fatiga():
        try:
            with open("fatiga.json", "r") as file:
                data = json.load(file)
            return data.get("porcentaje_fatiga", 0)  # Devuelve 0 si no existe
        except FileNotFoundError:
            return 0  # Si no hay archivo, usa un valor por defecto
        
    def obtener_porcentaje_fatiga2():
        try:
            with open("fatiga2.json", "r") as file:
                data = json.load(file)
            return data.get("porcentaje_fatiga2", 0)  # Devuelve 0 si no existe
        except FileNotFoundError:
            return 0  # Si no hay archivo, usa un valor por defecto
        
    def obtener_capacidad_perceptiva():
        try:
            with open("capacidad_perceptiva.json", "r") as file:
                data = json.load(file)
            return data.get("capacidad_perceptiva", 0)  # Devuelve 0 si no existe
        except FileNotFoundError:
            return 0  # Si no hay archivo, usa un valor por defecto
    
    def abrir_resultados():
        # Crear una nueva ventana para mostrar los resultados
        ventana_resultados = tk.Toplevel(ventana)
        ventana_resultados.title("Resultados")
        ventana_resultados.state("zoomed")
        ventana_resultados.configure(bg="#000000")
        
        titulo_resultados = tk.Label(
            ventana_resultados,
            text="Resultados",
            font=("Hello Valentica", 60, "bold"),
            fg="white",
            bg="#000000"
        )
        titulo_resultados.pack(pady=20)

        frame_resultados = tk.Frame(ventana_resultados, bg="#000000")
        frame_resultados.pack(pady=20, padx=50, fill="both", expand=True)

        resultado = obtener_resultados_bd()

        if not resultado:
            label_resultados = tk.Label(
                frame_resultados,
                text="No hay resultados disponibles.",
                font=("Arial", 24),
                fg="white",
                bg="#000000"
            )
            label_resultados.pack(pady=20)
        else:
            FA1 = obtener_porcentaje_fatiga()  # ✅ Obtener el valor desde el JSON
            FA2 = obtener_porcentaje_fatiga2()  # ✅ Obtener el porcentaje de fatiga de la actividad 2
            CAP = obtener_capacidad_perceptiva()  # ✅ Obtener capacidad perceptiva desde JSON

            # Definir otras variables necesarias para la fórmula
            W1 = 0.34
            W2 = 0.34
            W3 = 0.33

            # ✅ Calcular la ecuación con `FA1`
            resultado_formula = ((W1 * FA1) + (W2 * FA2) + (100 - CAP) * W3) / (W1 + W2 + W3)

            resultado_texto = (
                f"Tiempo Total: {resultado[1]:.2f} segundos\n"
                f"Aciertos: {resultado[2]}\n"
                f"Errores: {resultado[3]}\n"
                f"Omisiones: {resultado[4]}\n"
                f"IGAP: {resultado[5]}\n"
                f"Capacidad Perceptiva: {resultado[6]}%\n"
                f"Resultado general de fatiga: {resultado_formula:.2f}%\n"
                "-----------------------------------"
            )

            label_resultado = tk.Label(
                frame_resultados,
                text=resultado_texto,
                font=("Arial", 16),
                fg="white",
                bg="#000000",
                justify="left"
            )
            label_resultado.pack(pady=10)

        def generar_pdf():
            nombre_pdf = "resultados.pdf"
            resultados = obtener_resultados_bd()

            if not resultados:
                messagebox.showerror("Error", "No hay resultados disponibles para generar el PDF.")
                return

            c = pdf_canvas.Canvas(nombre_pdf, pagesize=letter)
            width, height = letter

            # Establecer la fuente
            c.setFont("Helvetica-Bold", 18)
            c.drawString(200, height - 50, "Resultados del Test")

            c.setFont("Courier", 12)
            y_position = height - 100  
            
            # Obtener la fecha (asumiendo que es el primer valor de la tupla)
            fecha = resultados[0]  # Si la fecha es el primer valor del resultado
            # Si la fecha es en formato 'YYYY-MM-DD HH:MM:SS', la dejamos como está.
            # Si no es así, la convertimos a un formato adecuado
            if isinstance(fecha, str):
                try:
                    # Convertir la fecha a un objeto datetime para asegurar que está en el formato adecuado
                    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
                    # Formatearla para mostrarla como 'DD-MM-YYYY HH:MM:SS'
                    fecha_formateada = fecha_obj.strftime('%d-%m-%Y %H:%M:%S')
                except ValueError:
                    # Si no es posible convertirla, usar la fecha tal como está
                    fecha_formateada = fecha
            else:
                fecha_formateada = str(fecha)

            # Iterar sobre los resultados
            for i in range(0, len(resultados), 7):  # Asumimos que cada grupo de 7 números es un conjunto de datos
                if i + 6 < len(resultados):  # Asegurarse de que hay suficientes datos
                    resultado_texto = (
                        #f"Fecha: {fecha_formateada}\n"
                        f"Tiempo Total: {resultados[i+1]:.2f} segundos\n"
                        f"Aciertos: {resultados[i+2]}\n"
                        f"Errores: {resultados[i+3]}\n"
                        f"Omisiones: {resultados[i+4]}\n"
                        f"IGAP: {resultados[i+5]:.2f}\n"
                        f"Capacidad Perceptiva: {resultados[i+6]:.2f}%\n"
                        "-----------------------------------"
                    )

                    for linea in resultado_texto.strip().split("\n"):
                        c.drawString(100, y_position, linea)
                        y_position -= 20  # Espaciado entre líneas

                    # Si ya no hay espacio en la página, crear una nueva
                    if y_position < 50:  
                        c.showPage()
                        c.setFont("Helvetica-Bold", 18)
                        c.drawString(200, height - 50, "Resultados del Test")
                        c.setFont("Courier", 12)
                        y_position = height - 100

            c.save()

            # Función para mostrar una ventana rosa personalizada
            def mostrar_ventana_resultado_pdf(mensaje):
                # Crear la ventana
                ventana_resultado_pdf = tk.Toplevel()
                ventana_resultado_pdf.title("Resultado del PDF")
                ventana_resultado_pdf.geometry("400x250+{}+{}".format(
                    (ventana_resultado_pdf.winfo_screenwidth() - 400) // 2,
                    (ventana_resultado_pdf.winfo_screenheight() - 200) // 2
                ))
                ventana_resultado_pdf.configure(bg="#D8A0FF")

                # Título de la ventana
                titulo = tk.Label(
                    ventana_resultado_pdf, text="MonitorMind",
                    font=("Hello Valentica", 30, "bold"),
                    fg="black", bg="#D8A0FF"
                )
                titulo.pack(pady=20)

                # Mensaje de la ventana
                mensaje_label = tk.Label(
                    ventana_resultado_pdf, 
                    text=mensaje,
                    font=("Milky Vintage", 16), 
                    fg="black", bg="#D8A0FF",
                    wraplength=300
                )
                mensaje_label.pack(pady=20)

                # Botón para cerrar la ventana
                boton = tk.Button(
                    ventana_resultado_pdf, text="Aceptar",
                    command=ventana_resultado_pdf.destroy,
                    font=("Milky Vintage", 15),
                    bg="#B547FF", fg="black",
                    width=15, height=1, relief="flat"
                )
                boton.place(relx=0.5, rely=0.8, anchor="center")

            # Verificar si el archivo fue creado
            if os.path.exists(nombre_pdf):
                mensaje = f"Resultados guardados en {os.path.abspath(nombre_pdf)}"
                mostrar_ventana_resultado_pdf(mensaje)
            else:
                mensaje = "El PDF no se generó correctamente."
                mostrar_ventana_resultado_pdf(mensaje)
            
        # Botón para generar el PDF (Se mantiene fijo)
        boton_generar_pdf = tk.Button(
            ventana_resultados,
            text="Generar Resultados en PDF",
            font=("Arial", 18),
            bg="#D8A0FF",
            fg="black",
            command=generar_pdf
        )
        boton_generar_pdf.pack(pady=10)
        
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
        font=("Milky Vintage", 30),
        image=icono_resultados_tk,
        compound="left",
        bg="#D8A0FF",
        fg="black",
        width=350,
        height=80,
        command=abrir_resultados
    )
    boton_resultados.pack(pady=35)

# Iniciar la carga inmediatamente
ventana.after(500, cargar)  # Llamar a cargar después de 500 ms

# Ejecutar la ventana principal
ventana.mainloop()