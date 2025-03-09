import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import dlib
import time
import textwrap
import subprocess
import numpy as np
import os
import resultados2


class MonitorMindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MonitorMind")
        self.root.state("zoomed")
        self.root.configure(bg="black")  # Fondo negro para la ventana principal

        # Obtén la ruta del directorio donde se encuentra el script
        directorio_actual = os.path.dirname(__file__)
        self.bostezo_detectado = False 

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

        # Cronómetro
        self.timer_running = False
        self.start_time = None
        self.timer_label = tk.Label(
            self.root, text="Tiempo: 00:00", font=("Arial", 16), bg="black", fg="white"
        )
        self.timer_label.place(relx=0.7, rely=0.3, anchor="center")

        # Instrucciones
        instrucciones_text = (
            "En la siguiente actividad deberá dar click únicamente" 
            " en las letras A, E y R. "
            
        )
        instrucciones_label = tk.Label(
            self.root, text=instrucciones_text, font=("Milky Vintage", 16), bg="black", fg="white", wraplength=400, justify="left"
        )
        instrucciones_label.place(relx=0.1, rely=0.45, anchor="w")  # Ajusta la posición según sea necesario

        
        # Zona de texto para la actividad con un recuadro
        self.text_frame = tk.Frame(self.root, bg="#F0E68C", width=500, height=400, bd=5, relief="raised")  # Recuadro más grande y color de fondo
        self.text_frame.place(relx=0.05, rely=0.6, anchor="w")

        self.text_label = tk.Label(
            self.text_frame, text="", font=("Arial", 18), bg="#F0E68C", fg="black", justify="center", wraplength=480
        )
        self.text_label.pack(pady=20)  # Añadir un poco de espacio alrededor del texto
        
        # Texto para la actividad
        self.text_lines = self.prepare_activity_text()
        self.current_line_index = 0
        self.selected_letters = {"A": 0, "E": 0, "R": 0}
        self.errors = 0

        # Zona donde se mostrará la imagen de la cámara
        self.video_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")  # Fondo gris para la cámara
        self.video_frame.place(relx=0.7, rely=0.6, anchor="center")
        self.canvas = tk.Canvas(self.video_frame, width=640, height=360, bg="#A7FFF2", highlightthickness=0)
        self.canvas.pack()

        # Botón único para iniciar la detección
        self.detect_button = tk.Button(
            self.root,
            text=" Iniciar Detección",
            font=("Milky Vintage", 18),
            bg="#D8A0FF",
            fg="black",
            image=self.camera_icon_tk,
            compound="left",
            width=200,
            height=50,
            command=self.start_detection
        )
        self.detect_button.place(relx=0.7, rely=0.93, anchor="center")
        
        self.regresar_button = tk.Button(
            self.root,
            text="Regresar",
            font=("Milky Vintage", 18),
            bg="#FFCCCB",
            fg="black",
            command=self.regresar
        )
        self.regresar_button.place(relx=0.9, rely=0.93, anchor="center")

        
        # Configuración de cámara
        self.cap = None
        self.camera_active = False
        self.detector = dlib.get_frontal_face_detector()
        

        # Cargar el predictor de landmarks usando una ruta relativa
        try:
            ruta_predictor = os.path.join(directorio_actual, "../assets/data/shape_predictor_68_face_landmarks.dat")
            self.predictor = dlib.shape_predictor(ruta_predictor)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'shape_predictor_68_face_landmarks.dat'")
        return

        # Variables de control
        self.detection_active = False
        self.yawn_count = 0

    def prepare_activity_text(self):
        full_text = (
            "Sobre una columna muy alta, dominando toda la ciudad, se alzaba la estatua del Príncipe Feliz. "
            "Estaba recubierta de oro fino y sus ojos eran dos grandes zafiros. "
            "Una noche de invierno llegó a la ciudad una golondrina y se refugió a los pies de la estatua. "
            "Cuando metía la cabeza bajo el ala, le cayó una gota de agua. "
            "- ¡Qué raro!, pensó, No hay nubes en el cielo, y sin embargo, llueve. "
            "Cayó una segunda gota y luego otra. La golondrina miró hacia arriba y vio que por las doradas mejillas del Príncipe rodaban gruesas lágrimas."
            "- ¿Por qué lloras?, le preguntó."
            "- Cuando estaba vivo, dijo la estatua, todo lo que veía en mi palacio era hermoso y alegre, por eso me llamaban el Príncipe Feliz. Pero ahora que ya no estoy vivo y me han colocado en este lugar tan alto, puedo ver la pobreza que hay en la ciudad y no puedo evitar llorar."
            "- ¿Y qué es lo que ves ahora?, preguntó la golondrina."
            "- Una casa muy pobre. Dentro hay una mujer bordando, y en un rincón está su hijo enfermo y hambriento. Pero la pobre, no tiene alimento que darle. Golondrina, ¿podrías llevarle el rubí de mi espada? Yo no puedo moverme de aquí."
            "Aunque hacía mucho frío, la golondrina aceptó y arrancando el rubí, salió volando con él en el pico. Llegó a la casa de la costurera, depositó el rubí sobre la caja de la costura de la mujer y abanicó la frente del niño con sus alas."
            "La golondrina volvió con el Príncipe Feliz y allí pasó la noche. Al día siguiente, le dijo al Príncipe."
            "- ¡Adiós! Mis compañeras me esperan para emigrar al sur."
            "- Por favor, golondrina, quédate, - le pidió el príncipe. Allá en una buhardilla veo a un joven escribiendo una obra de teatro para los niños. No tiene qué comer y se ha desmayado de hambre."
            "- Vale, me quedaré. ¿Qué debo llevarle?"
            "- El zafiro de uno de mis ojos, respondió el príncipe."
            "La golondrina, con gran pesar, le arrancó el rubí del ojo al Príncipe y se fue volando a la buhardilla. Cuando el escritor volvió en sí, exclamó: "
            "- ¡Oh, debe ser un regalo de algún admirador! Por fin podré terminar mi obra."
            "Al día siguiente la golondrina quiso marcharse a tierras más cálidas, el invierno estaba cerca, pero el Príncipe volvió a pedirle un favor más para ayudar a una niña muy pobre que vendía cerillas en una plaza. "
            "- ¡Quítame el rubí del otro ojo! Me quedaré ciego pero la niña tendrá con qué calentarse."
            "La golondrina accedió al deseo del Príncipe y se lo llevó a la niña que corrió emocionada a entregárselo a su madre. "
            "Al regresar junto al Príncipe, la generosa golondrina, le dijo al generoso Príncipe: "
            "- Ahora que estás ciego, no podré abandonarte. Volaré por la ciudad y te contré lo que vea."
            "- Arranca el oro que me cubre y dáselo a los pobres, le pidió el príncipe."
            "La golondrina así, repartió día tras día el oro de la estatua entre los pobres de toda la ciudad y así, llegaron las primeras nieves. La pequeña golondrina cada vez tenía más frío y procuraba calentarse batiendo las alas. Un día, sintió que iba a morir, se tumbó en el hombro del Príncipe y le dijo."
            "- ¡Querido Prínicipe! Ya no podré ir a Egipto, voy a morir, solo quiero decirte lo mucho que te amo."
            "La golondrina besó al príncipe y cayó muerta a sus pies. En ese mismo momento, se escuchó un crujido dentro de la estatua del príncipe. Era su corazón de plomo, partido en dos."   
        )
        self.total_letters = {
            "A": sum(1 for char in full_text if char.upper() == "A"),
            "E": sum(1 for char in full_text if char.upper() == "E"),
            "R": sum(1 for char in full_text if char.upper() == "R"),
        }
        return textwrap.wrap(full_text, width=30)

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

        # Activar detección
        self.detection_active = True
        self.yawn_count = 0
        self.bostezo_detectado = False  # Para evitar contar múltiples veces el mismo bostezo
        

        # Iniciar la actividad
        self.show_next_line()

    def update_timer(self):
        if not self.timer_running:
            return

        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.timer_label.config(text=f"Tiempo: {minutes:02d}:{seconds:02d}")

        if elapsed_time >= 180:  # 3 minutos
            self.stop_detection()
            messagebox.showinfo("Finalizado", "La detección ha terminado después de 3 minutos.")
        else:
            self.root.after(400, self.update_timer)

    def calculate_results(self):

        if idUser_sesion is None:
            messagebox.showerror("Error", "No se pudo identificar al usuario")
            return

        # Calcular tiempo empleado
        tiempo_fin = time.time()
        tiempo_ms = resultados2.calcular_tiempo_transcurrido(self.start_time, tiempo_fin)

        # Obtener los datos de selección de letras
        seleccionadas_a = self.selected_letters.get("A", 0)
        seleccionadas_e = self.selected_letters.get("E", 0)
        seleccionadas_r = self.selected_letters.get("R", 0)
        errores = self.errors
        bostezos = self.yawn_count  # Número de bostezos detectados durante la actividad

        # Guardar resultados en resultados2.txt
        resultados2.guardar_resultados(tiempo_ms, seleccionadas_a, seleccionadas_e, seleccionadas_r, errores, bostezos)

        # Mostrar mensaje final con los resultados
        resultados_texto = (
            f"Tiempo empleado: {tiempo_ms} ms\n"
            f"Letras 'A' seleccionadas: {seleccionadas_a}\n"
            f"Letras 'E' seleccionadas: {seleccionadas_e}\n"
            f"Letras 'R' seleccionadas: {seleccionadas_r}\n"
            f"Letras correctas seleccionadas: {selecionTotal}\n"
            f"Letras incorrectas seleccionadas: {errores}\n"
            f"Letras omitidas: {omisiones}\n"
            f"Bostezos detectados: {bostezos}\n"
        )

        messagebox.showinfo("Resultados", resultados_texto)

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
        self.current_line_index = len(self.text_lines)  # Evita que se sigan mostrando líneas
        self.root.after_cancel(self.show_next_line)  # Detiene el temporizador de la actividad

        # Mostrar resultados en lugar del mensaje de finalización
        self.calculate_results()

    def update_frame(self):
        if self.cap and self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                print("Frame capturado")  # Mensaje de depuración
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

            else:
                print("No se pudo capturar el frame")  # Mensaje de depuración

        if self.camera_active:
            self.root.after(30, self.update_frame)  # Aumentar el tiempo de espera


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

    def show_next_line(self):
        if not self.timer_running:  # Detén si el temporizador se detuvo
            return
        if self.current_line_index < len(self.text_lines):
            self.display_text_interactive(self.text_lines[self.current_line_index])
            self.current_line_index += 1
            self.root.after(8000, self.show_next_line)
        else:
            self.calculate_results()
            
    def regresar(self):
        self.stop_detection()  # Detener cualquier proceso activo
        self.root.destroy()  # Cerrar la ventana actual
        
        try:
            subprocess.run(["python", "seleccionarActividad.py"])  # Ejecutar el script de la otra interfaz
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo 'seleccionarActividad.py'")


    def display_text_interactive(self, line):
        for widget in self.text_frame.winfo_children():
            widget.destroy()

        for char in line:
            label = tk.Label(self.text_frame, text=char, font=("Milky Vintage", 20), bg="white", fg="black")
            if char.upper() in ["A", "E", "R"]:
                label.bind("<Button-1>", lambda event, c=char.upper(), l=label: self.select_letter(c, l, True))
            else:
                label.bind("<Button-1>", lambda event, c=char.upper(), l=label: self.select_letter(c, l, False))
            label.pack(side="left")

    def select_letter(self, letter, label, is_correct):
        if is_correct:
            label.config(fg="green")  # Marca la letra seleccionada
            self.selected_letters[letter] += 1
        else:
            label.config(fg="red")  # Marca el error
            self.errors += 1


if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorMindApp(root)
    root.mainloop()