import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
