import tkinter as tk
from tkinter import messagebox
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
        super().__init__(parent, padx=10, pady=10, borderwidth=2, relief="groove")
        self.refresh_callback = refresh_callback

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

        # Button to visualize gender distribution
        self.visualize_button = tk.Button(self, text="Visualize Gender Distribution",
                                          command=self.visualize_gender_distribution)
        self.visualize_button.pack(fill="x", pady=(0, 5))

    def submit_form(self):
        full_name = self.full_name_entry.get()
        email = self.email_entry.get()
        age = self.age_spinbox.get()
        gender = self.gender_var.get()

        

        if full_name and email and age and gender:
            db_handler = DatabaseHandler()
            db_handler.insert_user(full_name, email, age, gender)
            self.reset_form()
            self.refresh_callback()
        
    def reset_form(self):
        self.full_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_spinbox.delete(0, tk.END)
        self.age_spinbox.insert(0, "10")
        self.gender_var.set("")

    def visualize_gender_distribution(self):
        """Fetch gender counts from the database and show a pie chart in a new window.

        Uses messagebox to inform the user when there's no data or when an error occurs.
        """
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror(
                "Visualization Error",
                "matplotlib is not available; please install it (pip install matplotlib) to enable charting."
            )
            return

        try:
            students = DatabaseHandler.get_all_students()

            if not students:
                messagebox.showinfo("No data", "There are no registered students to visualize.")
                return

            # students: tuples (id, name, email, age, grade)
            male_count = 0
            female_count = 0
            other_count = 0

            for s in students:
                # gender stored in the 'grade' column for this schema
                gender_val = str(s[4]).strip().lower()
                if gender_val == 'male':
                    male_count += 1
                elif gender_val == 'female':
                    female_count += 1
                else:
                    other_count += 1

            labels = []
            sizes = []
            if male_count:
                labels.append('Male')
                sizes.append(male_count)
            if female_count:
                labels.append('Female')
                sizes.append(female_count)
            if other_count:
                labels.append('Other')
                sizes.append(other_count)

            if not sizes:
                messagebox.showinfo("No data", "There are no recognizable gender entries to visualize.")
                return

            # Create a new window to host the matplotlib figure
            win = tk.Toplevel(self)
            win.title("Gender Distribution")

            fig = Figure(figsize=(4, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ensures pie is drawn as a circle.

            canvas = FigureCanvasTkAgg(fig, master=win)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            # Use messagebox to show an error to the user
            messagebox.showerror("Visualization Error", f"An error occurred while visualizing: {e}")