from pandas import read_sql as pd_read_sql, read_csv as pd_read_csv, read_excel as pd_read_excel
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from xgboost import XGBClassifier
import json

model = XGBClassifier()
model.load_model("model.json")

class Prediction:
    W = 400
    H = 400

    def __init__(self, parent, by_name=None, by_file=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Predicción")
        self.window.geometry(f"{self.W}x{self.H}")
        self.window.resizable(False, False)

        # Create a Treeview widget
        self.treeview = ttk.Treeview(self.window, columns=("Column 1", "Column 2", "Column 3"), show="headings")
        self.treeview.pack(fill="both", expand=True)

        # Set column headings
        self.treeview.heading("Column 1", text="Email Usuario")
        self.treeview.heading("Column 2", text="Prob VIP")
        self.treeview.heading("Column 3", text="Prob No VIP")

        # Set column width
        self.treeview.column("Column 1", width=self.W//3)
        self.treeview.column("Column 2", width=self.W//3)
        self.treeview.column("Column 3", width=self.W//3)

        try:
            # load credentials
            with open("credenciales.json", 'r') as f:
                conn_data = json.load(f)

            self.DB_CONN = f'mysql+mysqlconnector://{conn_data["username"]}:{conn_data["password"]}@{conn_data["host"]}/{conn_data["database"]}'

            self.model = model

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar credenciales: {e}")

        # Predict
        if by_name is not None:
            self.predict_by_name(by_name)

        elif by_file is not None:
            self.predict_by_file(by_file)



    def add_row(self, name, prob_vip, prob_no_vip):
        self.treeview.insert("", "end", values=(name, prob_vip, prob_no_vip))

    def predict_by_name(self, name):
        try: 
            
            SQL = """ 
                SELECT
                    ad.Money,
                    LOWER(ad.Job) AS Job,
                    ad.Playtime_mins,
                    ad.JailTime,
                    ad.WL,
                    ad.Kills,
                    ad.Deaths,

                    COALESCE(ba.Balance, 0) AS Bank_money
                FROM accountdata ad
                LEFT JOIN bank_accounts ba ON ad.Username = ba.Account

                WHERE ad.Email = %s
            """

            data = pd_read_sql(SQL, self.DB_CONN, params=(name,))

            data = self.Preprocess_input(data)

            prob_no_vip, prob_vip = self.model.predict_proba(data)[0] * 100

            prob_no_vip = round(float(prob_no_vip), 2)
            prob_vip = round(float(prob_vip), 2)

            self.add_row(name, f"{prob_vip}%", f"{prob_no_vip}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer la prediccion por nombre: {e}")

    def predict_by_file(self, path):

        try:
            users = pd_read_csv(path, header=0, usecols=["Email"]).squeeze()

            # limpiar comillas
            users = users.str.replace("'", "")

            users_email = ",".join([f"'{user}'" for user in users])

            SQL = """ 
                SELECT
                    ad.Money,
                    LOWER(ad.Job) AS Job,
                    ad.Playtime_mins,
                    ad.JailTime,
                    ad.WL,
                    ad.Kills,
                    ad.Deaths,

                    COALESCE(ba.Balance, 0) AS Bank_money
                FROM accountdata ad
                LEFT JOIN bank_accounts ba ON ad.Username = ba.Account

                WHERE ad.Email IN (%s)
            """

            data = pd_read_sql(SQL % users_email, self.DB_CONN)
            data = self.Preprocess_input(data)

            probs = self.model.predict_proba(data) * 100

            for i, user in enumerate(users):
                prob_no_vip, prob_vip = probs[i]

                prob_no_vip = round(float(prob_no_vip), 2)
                prob_vip = round(float(prob_vip), 2)

                self.add_row(user, f"{prob_vip}%", f"{prob_no_vip}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al hacer la prediccion por archivo: {e}")


    def Preprocess_input(self, data):
        # PREPROCESAMIENTOS
        data.drop_duplicates(inplace=True)

        # filtrar y convertir variable Job a si tiene o no 
        data = data[~data["Job"].isin(["0", "banned"])]

        data["Job"] = data["Job"].map(lambda x: True if x not in ["unemployed", "none"] else False)

        return data        