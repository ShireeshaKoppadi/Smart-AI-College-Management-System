from flask import Flask, render_template, request, redirect, flash
import sqlite3
import pandas as pd
import os

from database import init_db

init_db()
app = Flask(__name__)

app.secret_key = "college123"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/students")
def students():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return render_template("students.html", students=students)

@app.route("/faculty")
def faculty():

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM faculty")

    faculty = cursor.fetchall()

    conn.close()

    return render_template(
        "faculty.html",
        faculty=faculty
    )

@app.route("/add_faculty", methods=["GET", "POST"])
def add_faculty():

    if request.method == "POST":

        name = request.form["name"]
        faculty_id = request.form["faculty_id"]
        department = request.form["department"]
        qualification = request.form["qualification"]
        experience = request.form["experience"]
        phone = request.form["phone"]
        email = request.form["email"]


        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO faculty
        (
        name,
        faculty_id,
        department,
        qualification,
        experience,
        phone,
        email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
        name,
        faculty_id,
        department,
        qualification,
        experience,
        phone,
        email
        ))


        conn.commit()
        conn.close()


        flash("Faculty Added Successfully!")

        return redirect("/faculty")


    return render_template("add_faculty.html")


@app.route("/delete_faculty/<int:id>")
def delete_faculty(id):

    conn=sqlite3.connect("college.db")
    cursor=conn.cursor()

    cursor.execute(
    "DELETE FROM faculty WHERE id=?",
    (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/faculty")

@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/prediction", methods=["GET", "POST"])
def prediction():

    result = None

    if request.method == "POST":

        attendance = float(request.form["attendance"])
        internal = float(request.form["internal"])
        assignment = float(request.form["assignment"])

        score = (attendance * 0.30) + (internal * 0.50) + (assignment * 0.20)

        if score >= 80:
            result = "Excellent"

        elif score >= 60:
            result = "Average"

        else:
            result = "Needs Improvement"

    return render_template("prediction.html", result=result)


@app.route("/add_student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]
        year = request.form["year"]
        phone = request.form["phone"]
        email = request.form["email"]
        cgpa = request.form.get("cgpa", "")
        attendance = request.form.get("attendance", "")
        marks = request.form.get("marks", "")

        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO students
        (name, roll, branch, year, phone, email, cgpa, attendance, marks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            roll,
            branch,
            year,
            phone,
            email,
            cgpa,
            attendance,
            marks
        ))

        conn.commit()
        conn.close()

        flash("Student Added Successfully!")

        return redirect("/students")

    return render_template("add_student.html")


@app.route("/search")
def search():

    query = request.args.get("query")

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%' + query + '%',)
    )

    students = cursor.fetchall()

    conn.close()

    return render_template("students.html", students=students)


@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Student Deleted Successfully")

    return redirect("/students")


@app.route("/edit_student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()


    if request.method == "POST":

        name = request.form["name"]
        roll = request.form["roll"]
        branch = request.form["branch"]
        year = request.form["year"]
        phone = request.form["phone"]
        email = request.form["email"]
        cgpa = request.form["cgpa"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]


        cursor.execute("""
        UPDATE students SET

        name=?,
        roll=?,
        branch=?,
        year=?,
        phone=?,
        email=?,
        cgpa=?,
        attendance=?,
        marks=?

        WHERE id=?

        """,
        (
        name,
        roll,
        branch,
        year,
        phone,
        email,
        cgpa,
        attendance,
        marks,
        id
        ))


        conn.commit()
        conn.close()

        return redirect("/students")


    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()


    return render_template(
        "edit_student.html",
        student=student
    )

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files["file"]

        if file.filename == "":
            flash("Please select a file")
            return redirect(request.url)


        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)


        if file.filename.endswith(".csv"):
            df = pd.read_csv(filepath)

        else:
            df = pd.read_excel(filepath)



        conn = sqlite3.connect("college.db")
        cursor = conn.cursor()


        for _, row in df.iterrows():

            cursor.execute("""
            INSERT INTO students
            (
            name,
            roll,
            branch,
            year,
            phone,
            email,
            cgpa,
            attendance,
            marks
            )

            VALUES (?,?,?,?,?,?,?,?,?)
            """,

            (
            row["name"],
            row["roll"],
            row["branch"],
            row["year"],
            row["phone"],
            row["email"],
            row["cgpa"],
            row["attendance"],
            row["marks"]
            ))


        conn.commit()
        conn.close()


        flash("Excel Data Uploaded Successfully!")

        return redirect("/students")


    return render_template("upload.html")







if __name__ == "__main__":
    app.run(debug=True)
