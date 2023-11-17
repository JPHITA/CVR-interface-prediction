import pandas as pd
import tkinter as tk
from xgboost import XGBClassifier
from threading import Thread

def load_model():
    from time import sleep

    global model

    sleep(0.1)

    model.load_model("model.json")
    # print("Modelo cargado")

model = XGBClassifier()
thread = Thread(target=load_model)
thread.start()

class Prediction:
    W = 400
    H = 400

    def __init__(self, parent, by_name=None, by_file=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Predicción")
        self.window.geometry(f"{self.W}x{self.H}")
        self.window.resizable(False, False)

        

