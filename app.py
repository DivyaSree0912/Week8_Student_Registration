
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("students.db")

def create_table():
    con = get_db()
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        con = get_db()
        con.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )
        con.commit()
        con.close()

        return redirect(url_for("students"))

    return render_template("register.html")

@app.route("/students")
def students():
    con = get_db()
    records = con.execute("SELECT * FROM students").fetchall()
    con.close()

    return render_template("students.html", students=records)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
