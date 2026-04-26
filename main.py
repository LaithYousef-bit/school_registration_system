import tkinter as tk
from tkinter import ttk
from Registerion_form import RegisterationForm
from Student_List import StudentList


class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("960x620")
        self.configure(bg="#f5f7fb")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Accent.TButton",
                             background="#383f4e",
                             foreground="#ffffff",
                             font=("Helvetica", 10, "bold"))
        self.style.configure("Card.TFrame", background="#ffffff")
        self.style.configure("Card.TLabel", background="#ffffff", foreground="#333333",
                             font=("Helvetica", 10))

        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#383f4e", height=90)
        header.pack(fill="x")

        title_label = tk.Label(header,
                               text="Student Management System",
                               bg="#383f4e",
                               fg="#ffffff",
                               font=("Helvetica", 24, "bold"))
        title_label.pack(pady=24)

        body = tk.Frame(self, bg="#f5f7fb")
        body.pack(fill="both", expand=True, padx=20, pady=10)

        self.registration_form = RegisterationForm(body, self.refresh_student_list)
        self.registration_form.pack(side="left", fill="y", padx=(0, 15), pady=10)

        separator = ttk.Separator(body, orient="vertical")
        separator.pack(side="left", fill="y", padx=10, pady=10)

        self.student_list = StudentList(body)
        self.student_list.pack(side="right", fill="both", expand=True, padx=(15, 0), pady=10)

    def refresh_student_list(self):
        self.student_list.read_students()


if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()
