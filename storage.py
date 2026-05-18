import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            api TEXT,
            summary TEXT,
            tests TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_run(api, summary, tests):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO runs (timestamp, api, summary, tests) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), api, json.dumps(summary), json.dumps(tests))
    )
    conn.commit()
    conn.close()

def list_runs(limit=20):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, timestamp, api, summary, tests FROM runs ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "timestamp": r[1],
            "api": r[2],
            "summary": json.loads(r[3]),
            "tests": json.loads(r[4])
        }
        for r in rows
    ]
