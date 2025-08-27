
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from student_tracker.tracker import StudentTracker
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

tracker = StudentTracker()

@app.route("/")
def index():
    students = tracker.all_students()
    return render_template("index.html", students=students)

@app.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll_number", "").strip()
        if not name or not roll.isdigit():
            flash("Please provide a valid name and numeric roll number.", "error")
            return redirect(url_for('add_student'))
        roll = int(roll)
        if tracker.add_student(name, roll):
            flash("Student added.", "success")
            return redirect(url_for('index'))
        else:
            flash("Roll number already exists.", "error")
    return render_template("add_student.html")

@app.route("/students/<int:roll_number>")
def view_student(roll_number):
    student = tracker.get_student(roll_number)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for('index'))
    return render_template("student_detail.html", student=student)

@app.route("/students/<int:roll_number>/grades", methods=["GET", "POST"])
def add_grades(roll_number):
    student = tracker.get_student(roll_number)
    if not student:
        flash("Student not found.", "error")
        return redirect(url_for('index'))

    if request.method == "POST":
        subjects = request.form.getlist("subject")
        scores = request.form.getlist("score")
        grades = {}
        for subj, sc in zip(subjects, scores):
            subj = subj.strip()
            if not subj:
                continue
            try:
                sc_val = float(sc)
            except ValueError:
                flash(f"Invalid score for {subj}.", "error")
                return redirect(url_for('add_grades', roll_number=roll_number))
            if 0 <= sc_val <= 100:
                grades[subj] = sc_val
            else:
                flash(f"Score for {subj} must be between 0 and 100.", "error")
                return redirect(url_for('add_grades', roll_number=roll_number))

        tracker.add_grades(roll_number, grades)
        flash("Grades updated.", "success")
        return redirect(url_for('view_student', roll_number=roll_number))

    return render_template("add_grades.html", student=student)

@app.route("/reports/topper")
def report_topper():
    subject = request.args.get("subject", "").strip()
    result = None
    if subject:
        result = tracker.subject_topper(subject)
    return render_template("class_reports.html", mode="topper", subject=subject, result=result)

@app.route("/reports/class-average")
def report_class_average():
    subject = request.args.get("subject", "").strip()
    avg = None
    if subject:
        avg = tracker.class_average(subject)
    return render_template("class_reports.html", mode="average", subject=subject, avg=avg)

@app.route("/backup/download")
def backup_download():
    path = tracker.backup_to_text("backup.txt")
    return send_file(path, as_attachment=True, download_name="student_backup.txt")

if __name__ == "__main__":
    # For local dev only
    app.run(debug=True, host="0.0.0.0", port=5000)
