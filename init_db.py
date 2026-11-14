
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Reset practice records
cursor.execute("DELETE FROM students")

# Reset SQLite auto-increment counter
cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name = 'students'"
)

# Five fictional practice records
students = [
    ("2026-00131", "Alex Rivera", "BSIT", 3, "A"),
    ("2026-00132", "Sofia Garcia", "BSIT", 2, "B"),
    ("2026-00133", "Daniel Cruz", "BSCS", 1, "A"),
    ("2026-00134", "Isabella Reyes", "BSIS", 3, "B"),
    ("2026-00135", "Gabriel Santos", "BSIT", 1, "C")
]

cursor.executemany("""
INSERT INTO students
(student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

connection.commit()
connection.close()

print("Database created successfully!")
print("Five student records inserted successfully!")
print("Database location:", DATABASE)
