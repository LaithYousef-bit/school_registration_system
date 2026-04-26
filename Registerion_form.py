import tkinter as tk
from tkinter import messagebox, ttk
from collections import Counter
from database_handler import DatabaseHandler

# Matplotlib imports for embedding charts in Tkinter.
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except Exception:
    Figure = None
    FigureCanvasTkAgg = None
    MATPLOTLIB_AVAILABLE = False


class RegisterationForm(tk.Frame):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent, bg="#ffffff", padx=20, pady=20, borderwidth=1, relief="solid")
        self.refresh_callback = refresh_callback

        self.full_name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.age_var = tk.StringVar(value="18")
        self.gender_var = tk.StringVar(value="Female")
        self.grade_var = tk.StringVar(value="A")

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Register New Student", bg="#ffffff",
                               fg="#333333", font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        subtitle_label = tk.Label(self,
                                  text="Add student details and watch analytics update instantly.",
                                  bg="#ffffff", fg="#666666", font=("Helvetica", 9))
        subtitle_label.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 16))

        self._add_row("Full Name", ttk.Entry(self, textvariable=self.full_name_var), 2)
        self._add_row("Email", ttk.Entry(self, textvariable=self.email_var), 3)
        self._add_row("Age", ttk.Spinbox(self, textvariable=self.age_var, from_=15, to=80, width=20), 4)

        gender_label = tk.Label(self, text="Gender", bg="#ffffff", fg="#444444", anchor="w")
        gender_label.grid(row=5, column=0, sticky="w", pady=(8, 2))
        gender_frame = tk.Frame(self, bg="#ffffff")
        gender_frame.grid(row=5, column=1, sticky="w", pady=(8, 2))
        tk.Radiobutton(gender_frame, text="Male", value="Male", variable=self.gender_var,
                       bg="#ffffff", anchor="w").pack(side="left", padx=(0, 8))
        tk.Radiobutton(gender_frame, text="Female", value="Female", variable=self.gender_var,
                       bg="#ffffff", anchor="w").pack(side="left")

        grade_label = tk.Label(self, text="Grade", bg="#ffffff", fg="#444444", anchor="w")
        grade_label.grid(row=6, column=0, sticky="w", pady=(8, 2))
        grade_combo = ttk.Combobox(self, textvariable=self.grade_var,
                                   values=["A", "B", "C", "D", "E", "F"], state="readonly",
                                   width=18)
        grade_combo.grid(row=6, column=1, sticky="ew", pady=(8, 2))
        grade_combo.current(0)

        self.submit_button = ttk.Button(self, text="Save Student", style="Accent.TButton",
                                        command=self.submit_form)
        self.submit_button.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(18, 8))

        self.clear_button = ttk.Button(self, text="Clear Fields", command=self.reset_form)
        self.clear_button.grid(row=8, column=0, columnspan=2, sticky="ew")

        self.visualize_button = ttk.Button(self, text="View Dashboard",
                                          style="Accent.TButton",
                                          command=self.visualize_statistics)
        self.visualize_button.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(16, 0))

        self.columnconfigure(1, weight=1)

    def _add_row(self, label_text, widget, row):
        label = tk.Label(self, text=label_text, bg="#ffffff", fg="#444444", anchor="w")
        label.grid(row=row, column=0, sticky="w", pady=(8, 2))
        widget.grid(row=row, column=1, sticky="ew", pady=(8, 2))

    def submit_form(self):
        full_name = self.full_name_var.get().strip()
        email = self.email_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()
        grade = self.grade_var.get().strip()

        if not full_name or not email or not age or not gender or not grade:
            messagebox.showwarning("Missing Data", "Please complete all fields before submitting.")
            return

        try:
            DatabaseHandler.insert_user(full_name, email, age, gender, grade)
            self.reset_form()
            self.refresh_callback()
            messagebox.showinfo("Saved", "Student profile saved successfully.")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save the student.\nDetails: {exc}")

    def reset_form(self):
        self.full_name_var.set("")
        self.email_var.set("")
        self.age_var.set("18")
        self.gender_var.set("Female")
        self.grade_var.set("A")

    def visualize_statistics(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror(
                "Visualization Error",
                "matplotlib is not available; please install it (pip install matplotlib) to enable charts."
            )
            return

        try:
            students = DatabaseHandler.get_all_students()
            if not students:
                messagebox.showinfo("No data", "There are no registered students to visualize.")
                return

            gender_counts = Counter(student[4] for student in students)
            grade_counts = Counter(student[5] for student in students)

            win = tk.Toplevel(self)
            win.title("Student Dashboard")
            win.configure(bg="#ffffff")

            fig = Figure(figsize=(8, 4), dpi=100)
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)

            gender_labels = list(gender_counts.keys())
            gender_sizes = list(gender_counts.values())
            ax1.pie(gender_sizes,
                    labels=gender_labels,
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=["#4a76d8", "#5cb85c", "#f0ad4e"])
            ax1.set_title("Gender Distribution")
            ax1.axis("equal")

            sorted_grades = sorted(grade_counts.keys())
            grade_values = [grade_counts[grade] for grade in sorted_grades]
            ax2.bar(sorted_grades, grade_values,
                    color=["#4a76d8", "#5cb85c", "#f0ad4e", "#d9534f", "#7d5a97", "#4d4d4d"][:len(sorted_grades)])
            ax2.set_title("Grade Distribution")
            ax2.set_xlabel("Grade")
            ax2.set_ylabel("Students")

            fig.tight_layout(pad=3.0)
            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        except Exception as exc:
            messagebox.showerror("Visualization Error", f"An error occurred while visualizing: {exc}")
