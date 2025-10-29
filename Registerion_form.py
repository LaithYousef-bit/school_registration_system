import tkinter as tk
from database_handler import DatabaseHandler

class RegisterationForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10, borderwidth=2, relief="groove")

        tk.Label(self, text="Full Name").pack(fill="x")
        self.full_name_entry = tk.Entry(self)
        self.full_name_entry.pack(fill="x")

        tk.Label(self, text="Email").pack(fill="x")
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(fill="x")

        tk.Label(self, text="Age").pack(fill="x")
        self.age_spinbox = tk.Spinbox(self, from_=10, to=100)
        self.age_spinbox.pack(fill="x")

        tk.Label(self, text="Gender").pack(fill="x")
        self.gender_var = tk.StringVar()
        tk.Radiobutton(self, text="Male", value="Male", variable=self.gender_var).pack(anchor="w")
        tk.Radiobutton(self, text="Female", value="Female", variable=self.gender_var).pack(anchor="w")

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.pack(fill="x", pady=5)

    def submit_form(self):
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        age = self.age_spinbox.get()
        gender = self.gender_var.get()

        print("Form submitted!")

        if full_name and email and age and gender:
            db_handler = DatabaseHandler()
            db_handler.insert_user(full_name, email, age, gender)
            self.reset_form()
            
    def reset_form(self):
        self.full_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_spinbox.delete(0, tk.END)
        self.age_spinbox.insert(0, "10")
        self.gender_var.set("")