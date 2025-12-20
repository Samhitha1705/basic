from flask import Flask, render_template, request, redirect, session
from db import init_db, create_user, validate_user, update_login, get_all_users, DB_DIR

app = Flask(__name__, template_folder="../frontend/templates")
app.secret_key = "supersecretkey"

# Initialize DB
init_db()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]

    try:
        create_user(username, password)
        return redirect("/")
    except:
        return "User already exists"


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if validate_user(username, password):
        session["user"] = username
        update_login(username)
        return redirect("/dashboard")

    return "Invalid credentials"


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    users = get_all_users()
    return render_template("dashboard.html", users=users)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    import traceback
    print(f"🚀 Starting Flask app on port 5002")
    print(f"DB path: {DB_DIR}/users.db")
    try:
        app.run(host="0.0.0.0", port=5002)
    except Exception:
        print("❌ Flask app failed to start:")
        traceback.print_exc()
        raise
