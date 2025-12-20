from flask import Flask, render_template, request, redirect, session
from db import init_db, create_user, validate_user, update_login, get_all_users

app = Flask(__name__, template_folder="../frontend/templates")
app.secret_key = "supersecretkey"

# Initialize DB safely
try:
    init_db()
except Exception as e:
    print(f"❌ Failed to initialize DB: {e}")

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return "Username and password are required", 400
    try:
        create_user(username, password)
        return redirect("/")
    except ValueError as ve:
        return str(ve), 400
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return "Internal Server Error", 500

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return "Username and password are required", 400

    if validate_user(username, password):
        session["user"] = username
        try:
            update_login(username)
        except Exception as e:
            print(f"❌ Failed to update login: {e}")
        return redirect("/dashboard")

    return "Invalid credentials", 401

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    try:
        users = get_all_users()
    except Exception as e:
        print(f"❌ Failed to get users: {e}")
        users = []
    return render_template("dashboard.html", users=users)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    print("🚀 Starting Flask app...")
    print(f"DB path: {DB_DIR}/users.db")
    app.run(host="0.0.0.0", port=5002)
