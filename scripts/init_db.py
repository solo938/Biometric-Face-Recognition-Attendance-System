import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY, name TEXT NOT NULL,
            department TEXT, embedding BLOB NOT NULL)""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT, emp_id TEXT,
            date TEXT, check_in_time TEXT, status TEXT DEFAULT 'Present',
            FOREIGN KEY(emp_id) REFERENCES employees(emp_id),
            UNIQUE(emp_id, date))""")
    conn.commit(); conn.close()
    print(f"Database ready: {DB_PATH}")

if __name__ == "__main__":
    init_db()
