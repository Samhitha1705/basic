import sqlite3
import os
from datetime import datetime

# Use container path for DB
DB_DIR = "/app/data"
DB_PATH = os.path.join(DB_DIR, "users.db")

# Ensure data folder exists
os.makedirs(DB_DIR, exist_ok=True)

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        print(f"❌ ERROR connecting to DB: {e}")
        raise

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                login_count INTEGER DEFAULT 0,
                last_login TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print(f"✅ users.db initialized at {DB_PATH}")
    except Exception as e:
        print(f"❌ ERROR initializing DB: {e}")
        raise

def create_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        print(f"✅ User '{username}' created")
    except sqlite3.IntegrityError:
        raise ValueError(f"User '{username}' already exists")
    except Exception as e:
        print(f"❌ ERROR creating user: {e}")
        raise

def validate_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(f"❌ ERROR validating user: {e}")
        return None

def update_login(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET login_count = login_count + 1,
                last_login = ?
            WHERE username = ?
        """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
        conn.commit()
        conn.close()
        print(f"✅ Updated login for '{username}'")
    except Exception as e:
        print(f"❌ ERROR updating login: {e}")

def get_all_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, last_login, login_count FROM users"
        )
        users = cursor.fetchall()
        conn.close()
        return users
    except Exception as e:
        print(f"❌ ERROR fetching users: {e}")
        return []
