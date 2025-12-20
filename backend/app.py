from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from db import init_db, create_user, validate_user, update_login

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(), "frontend", "templates")
)

app.secret_key = "supersecret"

# Initialize DB
init_db()

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = validate_user(username, password)

    if user:
        update_login(username)
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

        try:
            create_user(username, password)
            flash("User registered successfully!", "success")
            return redirect(url_for("index"))
        except Exception:
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
