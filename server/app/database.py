import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "editform.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            video_type TEXT NOT NULL,
            duration TEXT,
            budget TEXT,
            material_url TEXT,
            reference_url TEXT,
            notes TEXT,
            status TEXT DEFAULT '待处理',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
