
import os
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "students.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================
# HOME PAGE
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')


# ==========================================
# LABORATORY ACTIVITY 4-6
# BASIC FLASK API
# ==========================================

@app.route('/student', methods=['GET'])
def get_student():
    return jsonify({
        "student_id": "2026-00123",
        "name": "John Michael Bautista",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


@app.route('/hello', methods=['GET'])
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


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


# ==========================================
# LABORATORY ACTIVITY 7
# SQLITE DATABASE API
# ==========================================

# GET ALL STUDENTS
@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students ORDER BY id'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# GET ONE STUDENT BY DATABASE ID
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


# FILTER STUDENTS BY PROGRAM
@app.route('/students/program/<program>', methods=['GET'])
def get_students_by_program(program):
    conn = get_db_connection()

    students = conn.execute(
        """
        SELECT * FROM students
        WHERE UPPER(program) = UPPER(?)
        ORDER BY id
        """,
        (program,)
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# ==========================================
# LABORATORY ACTIVITY 8
# CREATE - READ - UPDATE - DELETE
# ==========================================

# HELPER: VALIDATE STUDENT DATA
def validate_student_data(data):
    required_fields = [
        'student_id',
        'name',
        'program',
        'year',
        'section'
    ]

    if not isinstance(data, dict):
        return None, "A valid JSON object is required."

    for field in required_fields:
        value = data.get(field)

        if value is None or str(value).strip() == '':
            return None, f"{field} is required."

    try:
        year = int(data['year'])
    except (ValueError, TypeError):
        return None, "Year must be a whole number."

    if year < 1:
        return None, "Year must be at least 1."

    cleaned_data = (
        str(data['student_id']).strip(),
        str(data['name']).strip(),
        str(data['program']).strip().upper(),
        year,
        str(data['section']).strip().upper()
    )

    return cleaned_data, None


# READ ALL STUDENTS
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()

    students = conn.execute(
        'SELECT * FROM students ORDER BY id'
    ).fetchall()

    conn.close()

    return jsonify([dict(student) for student in students])


# CREATE A STUDENT
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json(silent=True)
    student_data, error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO students
        (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)
        """,
        student_data
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "Student added successfully.",
        "id": new_id
    }), 201


# READ ONE STUDENT
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()

    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if student is None:
        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify(dict(student))


# UPDATE A STUDENT
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json(silent=True)
    student_data, error = validate_student_data(data)

    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()

    existing = conn.execute(
        'SELECT id FROM students WHERE id = ?',
        (id,)
    ).fetchone()

    if existing is None:
        conn.close()
        return jsonify({
            "error": "Student not found."
        }), 404

    conn.execute(
        """
        UPDATE students
        SET student_id = ?,
            name = ?,
            program = ?,
            year = ?,
            section = ?
        WHERE id = ?
        """,
        student_data + (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student updated successfully."
    })


# DELETE A STUDENT
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    cursor = conn.execute(
        'DELETE FROM students WHERE id = ?',
        (id,)
    )

    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({
            "error": "Student not found."
        }), 404

    return jsonify({
        "message": "Student deleted successfully."
    })


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
