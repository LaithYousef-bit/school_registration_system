import sqlite3


class DatabaseHandler:
    DB_NAME = "students.db"
    EXPECTED_COLUMNS = ["id", "name", "email", "age", "gender", "grade"]
    SAMPLE_STUDENTS = [
        ("Amina Khalid", "amina.khalid@example.com", 18, "Female", "A"),
        ("Omar Hassan", "omar.hassan@example.com", 19, "Male", "B"),
        ("Maya Farah", "maya.farah@example.com", 20, "Female", "A"),
        ("Karim Nasser", "karim.nasser@example.com", 21, "Male", "C"),
        ("Leila Samir", "leila.samir@example.com", 22, "Female", "B"),
        ("Yusuf Adel", "yusuf.adel@example.com", 23, "Male", "B"),
        ("Dina Youssef", "dina.youssef@example.com", 20, "Female", "A"),
        ("Nour El-Sayed", "nour.sayed@example.com", 19, "Female", "A"),
        ("Tarek Mostafa", "tarek.mostafa@example.com", 24, "Male", "C"),
        ("Sara Mahmoud", "sara.mahmoud@example.com", 18, "Female", "A"),
    ]

    @staticmethod
    def _connect():
        return sqlite3.connect(DatabaseHandler.DB_NAME)

    @staticmethod
    def create_table():
        with DatabaseHandler._connect() as conn:
            conn.execute(
                """CREATE TABLE IF NOT EXISTS students
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    grade TEXT NOT NULL);"""
            )

    @staticmethod
    def _table_exists():
        with DatabaseHandler._connect() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='students';"
            )
            return cursor.fetchone() is not None

    @staticmethod
    def _get_columns():
        with DatabaseHandler._connect() as conn:
            cursor = conn.execute("PRAGMA table_info(students);")
            return [row[1] for row in cursor.fetchall()]

    @staticmethod
    def _is_schema_current():
        return DatabaseHandler._get_columns() == DatabaseHandler.EXPECTED_COLUMNS

    @staticmethod
    def _should_reset_sample_data():
        with DatabaseHandler._connect() as conn:
            cursor = conn.execute("SELECT name, email FROM students;")
            rows = cursor.fetchall()
            if not rows:
                return True
            for name, email in rows:
                if "test" in (name or "").lower() or "test" in (email or "").lower():
                    return True
            return False

    @staticmethod
    def _seed_sample_data(conn):
        conn.executemany(
            """INSERT INTO students(name, email, age, gender, grade)
               VALUES (?, ?, ?, ?, ?);""",
            DatabaseHandler.SAMPLE_STUDENTS,
        )

    @staticmethod
    def initialize_database():
        needs_reset = False
        if not DatabaseHandler._table_exists():
            needs_reset = True
        elif not DatabaseHandler._is_schema_current():
            with DatabaseHandler._connect() as conn:
                conn.execute("DROP TABLE IF EXISTS students;")
            needs_reset = True
        elif DatabaseHandler._should_reset_sample_data():
            with DatabaseHandler._connect() as conn:
                conn.execute("DELETE FROM students;")
                DatabaseHandler._seed_sample_data(conn)

        if needs_reset:
            with DatabaseHandler._connect() as conn:
                conn.execute(
                    """CREATE TABLE students
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        grade TEXT NOT NULL);"""
                )
                DatabaseHandler._seed_sample_data(conn)

    @staticmethod
    def insert_user(name, email, age, gender, grade):
        with DatabaseHandler._connect() as conn:
            conn.execute(
                """INSERT INTO students(name, email, age, gender, grade)
                   VALUES (?, ?, ?, ?, ?);""",
                (name.strip(), email.strip(), int(age), gender.strip(), grade.strip()),
            )

    @staticmethod
    def get_all_students():
        with DatabaseHandler._connect() as conn:
            cursor = conn.execute("SELECT * FROM students;")
            return cursor.fetchall()


DatabaseHandler.initialize_database() 