from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecret"

DB_FILE = "data/users.db"
os.makedirs("data", exist_ok=True)

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session["username"] = username
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("Invalid credentials", "danger")
        return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", "")

        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                      (username, password, email))
            conn.commit()
            conn.close()
            flash("User registered successfully!", "success")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("index"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
