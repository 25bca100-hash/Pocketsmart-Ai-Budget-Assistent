import sqlite3

DATABASE = "pocketsmart.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            budget REAL NOT NULL,
            recommendation TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = get_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def login_user(username, password):
    conn = get_connection()

    user = conn.execute(
        """
        SELECT * FROM users
        WHERE username = ? AND password = ?
        """,
        (username, password)
    ).fetchone()

    conn.close()

    return user


def save_history(username, category, budget, recommendation):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO history
        (username, category, budget, recommendation)
        VALUES (?, ?, ?, ?)
        """,
        (username, category, budget, recommendation)
    )

    conn.commit()
    conn.close()


def get_history(username):
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    ).fetchall()

    conn.close()

    return rows