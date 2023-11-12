import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd

class PredictiveModelApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Colombian Virtual Reality")
        self.master.geometry("800x700")

        # Frame para la imagen de fondo
        self.image_frame = tk.Frame(master)
        self.image_frame.pack(fill="both", expand=True)

        # Cargar la imagen de fondo y redimensionarla al tamaño de la pantalla
        background_image = Image.open("image/CVR2.jpg")
        background_image = background_image.resize((800, 700))
        background_photo = ImageTk.PhotoImage(background_image)

        # Configurar el contenedor de la imagen de fondo
        self.background_label = tk.Label(self.image_frame, image=background_photo)
        self.background_label.image = background_photo
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame para los botones de predicción
        self.prediction_frame = tk.Frame(master, bg="navy")  # Establecer el color de fondo a azul marino
        self.prediction_frame.pack(fill="both", expand=True)

        # Variables para almacenar las entradas del usuario
        font_size = 12
        label_font = ("Arial", font_size, "bold")
        entry_font = ("Arial", font_size)
        button_font = ("Arial", font_size, "bold")

        self.name_label = tk.Label(self.prediction_frame, text="Nombre del Usuario:", font=label_font, bg="navy",
                                   fg="white")
        self.name_label.grid(row=0, column=0, pady=10, padx=10, sticky="e")

        self.name_entry = tk.Entry(self.prediction_frame, font=entry_font)
        self.name_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Botones para realizar la predicción
        self.predict_button = tk.Button(self.prediction_frame, text="Predecir por Nombre", command=self.predict_by_name,
                                        font=button_font, bg="white", fg="navy")
        self.predict_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        self.predict_file_button = tk.Button(self.prediction_frame, text="Predecir por Archivo",
                                             command=self.predict_by_file, font=button_font, bg="white", fg="navy")
        self.predict_file_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Etiqueta para mostrar el resultado de la predicción
        self.output_label = tk.Label(self.prediction_frame, text="", font=label_font, bg="navy", fg="white")
        self.output_label.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Configurar el peso de las filas y columnas para que se expandan con la ventana
        self.prediction_frame.grid_rowconfigure(0, weight=1)
        self.prediction_frame.grid_rowconfigure(1, weight=1)
        self.prediction_frame.grid_rowconfigure(2, weight=1)
        self.prediction_frame.grid_rowconfigure(3, weight=1)
        self.prediction_frame.grid_columnconfigure(0, weight=1)
        self.prediction_frame.grid_columnconfigure(1, weight=1)

        # Inicializar con el frame de la imagen visible y el frame de predicción oculto
        self.show_image_frame()
        self.hide_prediction_frame()

        # Bind para detectar cambios de tamaño de ventana
        master.bind("<Configure>", self.on_window_resize)

        # Botón para cambiar entre frames
        self.switch_frame_button = tk.Button(master, text="Predecir", command=self.toggle_frames, font=button_font,
                                             bg="white", fg="navy")
        self.switch_frame_button.pack(pady=10, padx=10)

    def on_window_resize(self, event):
        # Redimensionar la imagen de fondo cuando cambie el tamaño de la ventana
        screen_width = event.width
        screen_height = event.height
        background_image = Image.open("ColombianVirtualReality\image\CVR.jpg")
        background_image = background_image.resize((screen_width, screen_height))
        background_photo = ImageTk.PhotoImage(background_image)
        self.background_label.config(image=background_photo)
        self.background_label.image = background_photo

    def toggle_frames(self):
        # Cambiar entre el frame de imagen y el frame de predicción
        if self.image_frame.winfo_ismapped():
            self.hide_image_frame()
            self.show_prediction_frame()
        else:
            self.show_image_frame()
            self.hide_prediction_frame()

    def show_image_frame(self):
        self.image_frame.pack(fill="both", expand=True)

    def hide_image_frame(self):
        self.image_frame.pack_forget()

    def show_prediction_frame(self):
        self.prediction_frame.pack(fill="both", expand=True)

    def hide_prediction_frame(self):
        self.prediction_frame.pack_forget()

    def predict_by_name(self):
        # Obtener el nombre ingresado por el usuario
        user_name = self.name_entry.get()

        # Llamar al modelo predictivo con el nombre del usuario (sustituir con tu lógica)
        prediction = self.predictive_model_by_name(user_name)

        # Mostrar el resultado en la etiqueta de salida
        self.output_label.config(text=f"Predicción para {user_name}: {prediction}")

    def predictive_model_by_name(self, user_name):
        # Lógica de predicción por nombre (sustituir con tu modelo real)
        # Aquí puedes llamar a tu modelo predictivo y obtener la probabilidad de compra
        # En este ejemplo ficticio, simplemente devolvemos un valor de prueba
        return 0.75

    def predict_by_file(self):
        # Abrir el cuadro de diálogo para seleccionar un archivo Excel
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx;*.xls")])

        if file_path:
            # Cargar datos desde el archivo Excel
            df = pd.read_excel(file_path)

            # Llamar al modelo predictivo con los datos del archivo (sustituir con tu lógica)
            predictions = self.predictive_model_by_file(df)

            # Mostrar el resultado en la etiqueta de salida
            self.output_label.config(text=f"Predicciones desde Archivo:\n{predictions}")

    def predictive_model_by_file(self, data_frame):
        # Lógica de predicción desde archivo (sustituir con tu modelo real)
        # Aquí puedes llamar a tu modelo predictivo para cada fila del DataFrame y obtener las probabilidades de compra
        # En este ejemplo ficticio, simplemente devolvemos valores de prueba
        return [0.8, 0.6, 0.9]  # Lista de probabilidades para cada fila

def main():
    root = tk.Tk()
    app = PredictiveModelApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()