import tkinter as tk
from Registerion_form import RegisterationForm
from Student_List import StudentList


class MyApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Management System")
        self.geometry("900x600")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Student Management System", font=("Helvetica", 12))
        title_label.pack(side="top")

        self.registration_form = RegisterationForm(self, self.refresh_student_list)
        self.registration_form.pack(side="left", fill="y", padx=10, pady=10)

        self.student_list = StudentList(self)
        self.student_list.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def refresh_student_list(self):
        self.student_list.read_students()


if __name__ == "__main__":
    app = MyApplication()
    app.mainloop()