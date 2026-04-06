import sqlite3

def get_connection():
    return sqlite3.connect("data/database.db", check_same_thread=False)

def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, name, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, name, password) VALUES (?, ?, ?)",
        (username, name, password)
    )

    conn.commit()
    conn.close()


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, name, password FROM users")
    users = cursor.fetchall()

    conn.close()
    return users