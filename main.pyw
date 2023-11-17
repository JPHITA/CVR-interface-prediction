import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from prediction import Prediction

class Main:

    H = 700
    W = 800

    def __init__(self, master):
        self.master = master
        self.master.title("Colombian Virtual Reality")
        self.master.geometry(F"{self.W}x{self.H}")
        self.master.resizable(False, False)

        # Frame para la imagen de fondo
        self.image_frame = tk.Frame(master)
        self.image_frame.pack(fill="both", expand=True)
        self.background_label = tk.Label(self.image_frame)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Cargar la imagen de fondo
        self.set_img_background(self.background_label, "image/CVR2.jpg")

        # Frame para los botones de predicción
        self.prediction_frame = tk.Frame(master)
        self.prediction_frame.pack(fill="both", expand=True)
        self.prediction_background_label = tk.Label(self.prediction_frame)
        self.prediction_background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Cargar la imagen de fondo
        self.set_img_background(self.prediction_background_label, "image/CVR.jpg")

        # Variables para almacenar las entradas del usuario
        font_size = 12
        label_font = ("Arial", font_size, "bold")
        entry_font = ("Arial", font_size)
        button_font = ("Arial", font_size, "bold")

        self.name_label = tk.Label(self.prediction_frame, text="Email del Usuario:", font=label_font)
        self.name_label.grid(row=0, column=0, pady=50, padx=10, sticky="e")

        self.name_entry = tk.Entry(self.prediction_frame, font=entry_font)
        self.name_entry.grid(row=0, column=1, pady=50, padx=10, sticky="w")

        # Botones para realizar la predicción
        self.predict_button = tk.Button(self.prediction_frame, text="Predecir por Email", command=self.predict_by_name,
                                        font=button_font, bg="white", width=20, height=2)
        self.predict_button.grid(row=1, column=0, columnspan=2, pady=2, padx=10)

        self.predict_file_button = tk.Button(self.prediction_frame, text="Predecir por Archivo",
                                             command=self.predict_by_file, font=button_font, bg="white", width=20, height=2)
        self.predict_file_button.grid(row=2, column=0, columnspan=2, pady=2, padx=10)

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


        # Botón para cambiar entre frames
        self.switch_frame_button = tk.Button(master, text="Predecir", command=self.toggle_frames, font=button_font,
                                             bg="white")
        self.switch_frame_button.pack(pady=10, padx=10)


    def set_img_background(self, element, path):
        # Cargar la imagen de fondo y redimensionarla al tamaño de la pantalla
        background_image = Image.open(path)
        background_image = background_image.resize((self.W, self.H))
        background_photo = ImageTk.PhotoImage(background_image)

        element.configure(image=background_photo)
        element.image = background_photo

    def toggle_frames(self):
        self.switch_frame_button.pack_forget()

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
        user_name = self.name_entry.get().strip()

        if len(user_name) > 0:
            Prediction(self.master, by_name=user_name)

        else:
            tk.messagebox.showerror("Error", "Ingrese un nombre de usuario válido")

    def predict_by_file(self):
        # Abrir el cuadro de diálogo para seleccionar un archivo Excel
        file_path = filedialog.askopenfilename(filetypes=[("Archivos csv", "*.csv")])

        if file_path:
            Prediction(self.master, by_file=file_path)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()