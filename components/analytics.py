# components/analytics.py
import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "db/gate_exam_history.db"

def initialize_db():
    """Creates the database tables if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # Table for storing every generated question
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            question_type TEXT NOT NULL,
            question_text TEXT NOT NULL UNIQUE,
            options TEXT, -- JSON string
            answer TEXT NOT NULL, -- JSON string
            explanation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        # Table for storing test results
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

def save_test_result(topic, score, total_questions):
    """Saves a completed test's score and details to the history table."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO test_history (topic, score, total_questions) VALUES (?, ?, ?)",
            (topic, score, total_questions)
        )
        conn.commit()

def get_test_history():
    """Retrieves the entire test history as a Pandas DataFrame."""
    with sqlite3.connect(DB_FILE) as conn:
        df = pd.read_sql_query("SELECT topic, score, total_questions, test_date FROM test_history ORDER BY test_date DESC", conn)
    return df

# --- NEW FUNCTION ---
def get_questions_by_ids(ids: list[str]) -> list[dict]:
    """Retrieves full question details from the SQLite DB for a list of IDs."""
    if not ids:
        return []
    
    placeholders = ', '.join('?' for _ in ids)
    query = f"SELECT * FROM question_bank WHERE id IN ({placeholders})"
    
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row # Allows accessing columns by name
        cursor = conn.cursor()
        cursor.execute(query, ids)
        rows = cursor.fetchall()
        # Convert sqlite.Row objects to standard dictionaries
        return [dict(row) for row in rows]