import tkinter as tk
from Registerion_form import RegisterationForm
class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Student Management System", font=("Helvetica", 12))
        title_label.pack(side="top")

        self.registration_form = RegisterationForm(self)
        self.registration_form.pack(side="left", fill="y", padx=10, pady=10)


if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()