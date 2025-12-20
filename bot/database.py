import sqlite3
from pathlib import Path

DB_PATH = Path("database/users.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/users.sql", "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()


def add_user(tg_id: int, username: str, first_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (tg_id, username, first_name)
        VALUES (?, ?, ?)
    """, (tg_id, username, first_name))

    conn.commit()
    conn.close()


def add_view(tg_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users SET views = views + 1 WHERE tg_id = ?
    """, (tg_id,))

    conn.commit()
    conn.close()


def add_like(from_tg_id: int, to_tg_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO likes (from_tg_id, to_tg_id)
            VALUES (?, ?)
        """, (from_tg_id, to_tg_id))
        cursor.execute("""
            UPDATE users SET likes = likes + 1 WHERE tg_id = ?
        """, (to_tg_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()