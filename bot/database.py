import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database/users.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, first_name, last_name, username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (id, first_name, last_name, username)
        VALUES (?, ?, ?, ?)
    ''', (user_id, first_name, last_name, username))
    conn.commit()
    conn.close()

def update_views(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE users SET views = views + 1 WHERE id = ?', (user_id,))
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.commit()
    conn.close()
    return user