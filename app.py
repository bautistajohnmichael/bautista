
import sqlite3
import os

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# DATABASE LOCATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'students.db')


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# STUDENT INFORMATION API
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify({
        "student_id": "2026-00123",
        "name": "John Michael Bautista",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# GREETING API
@app.route('/hello', methods=['GET'])
def say_hello():
    name = request.args.get('name', 'Student')

    return jsonify({
        "message": f"Hello, {name}!"
    })


# CUSTOM API - SUBJECTS
@app.route('/subjects', methods=['GET'])
def get_subjects():
    return jsonify({
        "subjects": [
            {
                "code": "IT3120",
                "name": "System Integration",
                "professor": "Dr. Rene Arduo"
            },
            {
                "code": "IT3122",
                "name": "Quantitative",
                "professor": "Dr. Rene Arduo"
            },
            {
                "code": "ITPE3",
                "name": "Web Systems Technologies",
                "professor": "Dr. Weena Bulnes"
            }
        ]
    })


# DATABASE API - GET ALL STUDENTS
@app.route('/students', methods=['GET'])
def get_students():

    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# DATABASE API - GET ONE STUDENT BY ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student_by_id(id):

    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(dict(student))


# ADDITIONAL TASK - FILTER STUDENTS BY PROGRAM
@app.route('/students/program/<program>', methods=['GET'])
def get_students_by_program(program):

    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students WHERE program = ?',
        (program.upper(),)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# RUN APPLICATION
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
