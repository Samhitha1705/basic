import sqlite3
import os
from datetime import datetime

# Always use /app/data inside Docker
DB_DIR = "/app/data"
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "users.db")


def get_connection():
    """Return a SQLite connection to the database."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Initialize the database and create users table if not exists."""
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


def create_user(username, password):
    """Insert a new user into the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
    conn.close()


def validate_user(username, password):
    """Check if a user exists with the given credentials."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user


def update_login(username):
    """Update the last login time and increment login_count for a user."""
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


def get_all_users():
    """Return a list of all users with id, username, last_login, and login_count."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, last_login, login_count FROM users"
    )
    users = cursor.fetchall()
    conn.close()
    return users
