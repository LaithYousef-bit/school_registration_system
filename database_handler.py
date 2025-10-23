import sqlite3

class DatabaseHandler:
    DB_NAME = 'students.db'
 
    @staticmethod
    def _connect():
        return sqlite3.connect(DatabaseHandler.DB_NAME)

    @staticmethod
    def create_table():
        with DatabaseHandler._connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS students
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL,
                             email TEXT NOT NULL,
                             age INTEGER NOT NULL,
                             grade TEXT NOT NULL);''')
            
    @staticmethod
    def add_student(name, email, age, grade):
        with DatabaseHandler._connect() as conn:
            conn.execute('''INSERT INTO students (name, email, age, grade)
                            VALUES (?, ?, ?, ?);''', (name, email, age, grade))

    @staticmethod
    def get_all_students():
        with DatabaseHandler._connect() as conn:
            cursor = conn.execute('SELECT * FROM students;')
            return cursor.fetchall()     
                  

DatabaseHandler.create_table() 