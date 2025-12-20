import sqlite3
import os
from datetime import datetime

DB_DIR = "/app/data"
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "users.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Rest of your functions remain the same
