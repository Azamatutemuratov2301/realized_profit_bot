# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        login TEXT,
        password TEXT,
        server TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, login, password, server):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO users (user_id, login, password, server) VALUES (?, ?, ?, ?)",
                   (user_id, login, password, server))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
