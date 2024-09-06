import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

def create_connection():
    conn = sqlite3.connect(BASE_DIR / "todo.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_task(task):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todos")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_task(task_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, new_task):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET task = ? WHERE id = ?", (new_task, task_id))
    conn.commit()
    conn.close()
