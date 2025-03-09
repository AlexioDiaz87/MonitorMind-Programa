import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import dlib
import subprocess
import time
import numpy as np
import random
import os
import resultados3

class MonitorMindApp2:
    def __init__(self, root):
        self.root = root
        self.root.title("MonitorMind")
        self.root.state("zoomed")
        self.root.configure(bg="black")  # Fondo negro para la ventana principal

        # Obtén la ruta del directorio donde se encuentra el script
        directorio_actual = os.path.dirname(__file__)

        # Logo
        try:
            ruta_logo = os.path.join(directorio_actual, "../assets/images/cerebro.png")
            self.logo_image = Image.open(ruta_logo).resize((120, 120), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: cerebro.png")
            return

        # Cámara ícono
        try:
            ruta_camara = os.path.join(directorio_actual, "../assets/images/camara.png")
            self.camera_icon = Image.open(ruta_camara).resize((30, 30), Image.Resampling.LANCZOS)
            self.camera_icon_tk = ImageTk.PhotoImage(self.camera_icon)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo: camara.png")
            return

        # Título
        title_frame = tk.Frame(self.root, bg="black")
        title_frame.pack(pady=20)
        logo_label = tk.Label(title_frame, image=self.logo_photo, bg="black")
        logo_label.pack(side="left", padx=10)
        title_label = tk.Label(
            title_frame, text="MonitorMind", font=("Hello Valentica", 60, "bold"), bg="black", fg="white"
        )
        title_label.pack(side="left")

        # Título "Actividad"
        actividad_label = tk.Label(
            self.root, text="Actividad", font=("Milky Vintage", 30), bg="black", fg="white"
        )
        actividad_label.place(relx=0.1, rely=0.3, anchor="w")

        # Instrucciones
        instrucciones_text = (
            "En la siguiente actividad aparecerá en la pantalla distintas" 
            " figuras geométricas. Únicamente deberás hacer click cuando se"
            " muestre un triángulo."
        )
        instrucciones_label = tk.Label(
            self.root, text=instrucciones_text, font=("Milky Vintage", 16), bg="black", fg="white", wraplength=400, justify="left"
        )
        instrucciones_label.place(relx=0.1, rely=0.38, anchor="w")  # Ajusta la posición según sea necesario

        # Cronómetro
        self.timer_running = False
        self.start_time = None
        self.timer_label = tk.Label(
            self.root, text="Tiempo: 00:00", font=("Arial", 16), bg="black", fg="white"
        )
        self.timer_label.place(relx=0.7, rely=0.3, anchor="center")

        # Zona donde se mostrará la imagen de la cámara
        self.video_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")  # Fondo gris para la cámara
        self.video_frame.place(relx=0.7, rely=0.6, anchor="center")
        self.canvas = tk.Canvas(self.video_frame, width=640, height=360, bg="#A7FFF2", highlightthickness=0)
        self.canvas.pack()

        # Canvas para la actividad de clic
        self.activity_canvas = tk.Canvas(self.root, width=300, height=300, bg="#F3EEE1")
        self.activity_canvas.place(relx=0.1, rely=0.45, anchor="nw")  # Ajustar la posición más abajo

        # Variables para la actividad
        self.triangle_missed = 0  # Contador de omisiones de triángulos
        self.triangle_count = 0
        self.click_count = 0
        self.start_time_activity = None
        self.reaction_times = []
        self.correct_clicks = 0
        self.incorrect_clicks = 0

        # Botón único para iniciar la detección
        self.detect_button = tk.Button(
            self.root,
            text=" Iniciar Detección",
            font=("Milky Vintage", 20),
            bg="#D8A0FF",
            fg="black",
            image=self.camera_icon_tk,
            compound="left",
            width=215,
            height=50,
            command=self.start_detection
        )
        self.detect_button.place(relx=0.7, rely=0.93, anchor="center")
        
        self.regresar_button = tk.Button(
            self.root,
            text="Regresar",
            font=("Milky Vintage", 20),
            bg="#FFCCCB",
            fg="black",
            command=self.regresar
        )
        self.regresar_button.place(relx=0.9, rely=0.93, anchor="center")

        # Configuración de cámara
        self.cap = None
        self.camera_active = False
        self.detector = dlib.get_frontal_face_detector()

        # Variables de control
        self.detection_active = False
        self.yawn_count = 0
        self.bostezo_detectado = False  # Para evitar contar múltiples veces el mismo bostezo

        # Cargar el predictor de landmarks usando una ruta relativa
        try:
            ruta_predictor = os.path.join(directorio_actual, "../assets/data/shape_predictor_68_face_landmarks.dat")
            self.predictor = dlib.shape_predictor(ruta_predictor)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'shape_predictor_68_face_landmarks.dat'")
            return 

    def start_detection(self):
        
        # Crear la ventana de instrucciones
        ventana_instruccion = tk.Toplevel()
        ventana_instruccion.title("Advertencia")
        ventana_instruccion.geometry("300x200+{}+{}".format(
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
            text="Asegúrese de estar en un lugar bien iluminado.",
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
        
        if not self.camera_active:
            self.camera_active = True
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "No se puede acceder a la cámara")
                self.camera_active = False
                return
            self.update_frame()

        # Configuración del cronómetro
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self.update_timer()

        # Iniciar la actividad de clic
        self.start_activity()
        
    

    def update_timer(self):
        if not self.timer_running:
            return

        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.timer_label.config(text=f"Tiempo: {minutes:02d}:{seconds:02d}")

        if elapsed_time >= 120:  # 2 minutos
            self.stop_detection()
            messagebox.showinfo("Finalizado", "La detección ha terminado después de 2 minutos.")
        else:
            self.root.after(1000, self.update_timer)

    def stop_detection(self):
        self.timer_running = False
        self.detection_active = False

        # Detener la cámara
        if self.cap:
            self.cap.release()
            self.cap = None

        self.camera_active = False
        self.canvas.delete("all")
        self.timer_label.config(text="Tiempo: 00:00")

        # Detener la actividad
        self.activity_canvas.delete("all")  # Limpiar el canvas de actividad
        self.calculate_results2()

    def update_frame(self):
        if self.cap and self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector(gray)

                for face in faces:
                    landmarks = self.predictor(gray, face)
                    mar = self.calculate_mar(landmarks)

                    if mar > 0.5:  # Umbral para considerar un bostezo
                        if not self.bostezo_detectado:
                            self.yawn_count += 1  # Incrementa el contador solo una vez por bostezo
                            self.bostezo_detectado = True  # Marca que un bostezo fue detectado

                    else:
                        self.bostezo_detectado = False  # Se reinicia cuando la boca se cierra

                    # Dibujar puntos faciales
                    for n in range(48, 68):
                        x, y = landmarks.part(n).x, landmarks.part(n).y
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

                # Mostrar el texto "BOSTEZO DETECTADO" en el video
                if self.bostezo_detectado:
                    cv2.putText(frame, "BOSTEZO DETECTADO", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

                # Convertir frame para mostrar en la interfaz
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                self.img_tk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.img_tk, anchor="nw")

        if self.camera_active:
            self.root.after(10, self.update_frame)

    

    def calculate_mar(self, landmarks):
        top_lip = np.mean([landmarks.part(i).y for i in range(50, 53)])
        bottom_lip = np.mean([landmarks.part(i).y for i in range(65, 68)])
        vertical_distance = abs(top_lip - bottom_lip)

        left_lip = landmarks.part(48).x
        right_lip = landmarks.part(54).x
        horizontal_distance = abs(right_lip - left_lip)

        if horizontal_distance == 0:
            return 0
        return vertical_distance / horizontal_distance

    def regresar(self):
        self.stop_detection()  # Detener cualquier proceso activo
        self.root.destroy()  # Cerrar la ventana actual
        subprocess.run(["python", "seleccionarActividad.py"])  # Ejecutar el script de la otra interfaz
        
    def start_activity(self):
        self.triangle_count = 0
        self.click_count = 0
        self.start_time_activity = time.time()
        self.reaction_times = []
        self.correct_clicks = 0
        self.incorrect_clicks = 0
        self.show_random_shape()  # Cambiar a una sola figura

    def show_random_shape(self):
        if not self.timer_running:
            return

        self.activity_canvas.delete("all")
        shape_type = random.choice(["triangle", "circle", "square"])
        x, y = 100, 100

        if shape_type == "triangle":
            self.triangle_count +=1
            self.triangle_missed += 1  # Aumenta el contador de omisiones
            self.draw_triangle(x, y)
        elif shape_type == "circle":
            self.draw_circle(x, y)
        elif shape_type == "square":
            self.draw_square(x, y)

        self.activity_canvas.after(500, self.show_random_shape)

    def draw_triangle(self, x, y):
        self.triangle_appearance_time = time.time ()  
        triangle = self.activity_canvas.create_polygon(
            x, y, 
            x + 80, y + 140,  # Aumentado el tamaño
            x - 80, y + 140,  
            fill="yellow", outline="black"
        )
        self.activity_canvas.tag_bind(triangle, "<Button-1>", self.on_click_triangle)


    def draw_circle(self, x, y):
        circle = self.activity_canvas.create_oval(
            x, y, 
            x + 120, y + 120,  # Aumentado el tamaño
            fill="#03A5EE", outline="black"
        )
        self.activity_canvas.tag_bind(circle, "<Button-1>", self.on_click_wrong_figure)


    def draw_square(self, x, y):
        square = self.activity_canvas.create_rectangle(
            x, y, 
            x + 120, y + 120,  # Aumentado el tamaño
            fill="#CC00FF", outline="black"
        )
        self.activity_canvas.tag_bind(square, "<Button-1>", self.on_click_wrong_figure)


    def on_click_wrong_figure(self, event):
        self.incorrect_clicks += 1  # Aumentar el contador de figuras erróneas

        # Cambiar el color de la figura errónea al hacer clic
        figure_id = self.activity_canvas.find_closest(event.x, event.y)
        self.activity_canvas.itemconfig(figure_id, fill="#C10037")  # Cambiar color para indicar error


    def on_click_triangle(self, event):
        self.click_count += 1
        reaction_time = (time.time() - self.triangle_appearance_time) * 1_000  # Convertir a ms
        self.reaction_times.append(reaction_time)
        self.correct_clicks += 1
        self.triangle_missed -= 1  # Restar porque sí se seleccionó

        triangle_id = self.activity_canvas.find_closest(event.x, event.y)
        self.activity_canvas.itemconfig(triangle_id, fill="#5BDE44")


    def calculate_results(self):
        # Calcular tiempo empleado
        tiempo_fin = time.time()
        tiempo_ms = resultados3.calcular_tiempo_transcurrido(self.start_time, tiempo_fin)
        
        # Calcular VELOCIDAD DE REACCION
        if self.reaction_times:
            avg_reaction_time = (sum(self.reaction_times) / len(self.reaction_times)) if self.reaction_times else 0
        else:
            avg_reaction_time = 0  # Si no se hizo clic en ningún triángulo
        
        # Número de omisiones de triángulos (los que aparecieron y no se seleccionaron)
        omisiones_triángulo =abs(self.triangle_missed)

        # Obtener los datos de la actividad
        triangulos_seleccionados = self.correct_clicks  # Triángulos correctamente seleccionados
        errores_seleccionados = self.incorrect_clicks  # Figuras erróneas seleccionadas
        bostezos = self.yawn_count  # Número de bostezos detectados

        # Guardar resultados en resultados3.txt
        resultados3.guardar_resultados(tiempo_ms, triangulos_seleccionados, errores_seleccionados, bostezos, avg_reaction_time, omisiones_triángulo, porcentaje_fatiga2)

        resultados_texto = (
            f"Tiempo empleado: {tiempo_ms} ms\n"
            f"Tiempo de reacción promedio: {avg_reaction_time:.2f} ms\n"
            f"Triángulos seleccionados: {triangulos_seleccionados}\n"
            f"Omisiones de triángulos: {omisiones_triángulo}\n"
            f"Figuras erróneas seleccionadas: {errores_seleccionados}\n"
            f"Bostezos detectados: {bostezos}\n"
            f"Porcentaje de fatiga: {porcentaje_fatiga2:.2f}%\n"  # Muestra el porcentaje de fatiga
        )
        
        # Crear la ventana de instrucciones
        ventana_instruccion = tk.Toplevel()
        ventana_instruccion.title("Resultados")
        ventana_instruccion.geometry("300x300+{}+{}".format(
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
            text=resultados_texto,
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
        return porcentaje_fatiga2
        
        




if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorMindApp2(root)
    root.mainloop()