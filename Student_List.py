import tkinter as tk
from tkinter import ttk
from database_handler import DatabaseHandler


class StudentList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f7fb")
        self.create_widgets()

    def create_widgets(self):
        header = tk.Frame(self, bg="#f5f7fb")
        header.pack(fill="x", pady=(0, 12))

        title_label = tk.Label(header, text="Student Directory",
                               bg="#f5f7fb", fg="#333333",
                               font=("Helvetica", 15, "bold"))
        title_label.pack(anchor="w")

        self.count_label = tk.Label(header, text="", bg="#f5f7fb", fg="#555555",
                                    font=("Helvetica", 10))
        self.count_label.pack(anchor="w", pady=(2, 0))

        table_frame = tk.Frame(self, bg="#f5f7fb")
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Email", "Age", "Gender", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
        for col in columns:
            self.tree.heading(col, text=col)
            width = 40 if col == "ID" else 140 if col == "Email" else 80
            self.tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.read_students()

    def read_students(self):
        self.tree.delete(*self.tree.get_children())
        students = DatabaseHandler.get_all_students()
        for student in students:
            self.tree.insert("", tk.END, values=student)

        self.count_label.config(text=f"Total students: {len(students)}")
