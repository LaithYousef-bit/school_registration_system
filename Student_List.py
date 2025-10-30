import tkinter as tk
from tkinter import ttk
from database_handler import DatabaseHandler

class StudentList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Email", "Age", "Grade"),
                                       show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Grade", text="Grade")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.read_students()

    def read_students(self):
        self.tree.delete(*self.tree.get_children())
        for student in DatabaseHandler.get_all_students():
            self.tree.insert("", tk.END, values=student)
