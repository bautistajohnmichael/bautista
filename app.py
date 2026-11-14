
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


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


# RUN APPLICATION
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
