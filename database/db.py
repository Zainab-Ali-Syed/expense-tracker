import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_PATH = "spendly.db"

def get_db():
    """
    Opens connection to spendly.db in project root.
    Sets row_factory to sqlite3.Row and enables foreign keys.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Creates both tables using CREATE TABLE IF NOT EXISTS.
    Safe to call multiple times.
    """
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

def seed_db():
    """
    Inserts one demo user and 8 sample expenses.
    Prevents duplicate inserts if users already exist.
    """
    with get_db() as conn:
        # Check if users table already contains data
        cursor = conn.execute("SELECT count(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return

        # Insert demo user
        demo_password = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", demo_password)
        )
        user_id = cursor.lastrowid

        # Insert 8 sample expenses covering all 7 categories
        # Categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
        sample_expenses = [
            (user_id, 15.50, "Food", "2026-09-01", "Lunch at Cafe"),
            (user_id, 42.00, "Food", "2026-09-03", "Grocery shopping"),
            (user_id, 12.00, "Transport", "2026-09-05", "Uber ride"),
            (user_id, 85.00, "Bills", "2026-09-10", "Internet bill"),
            (user_id, 20.00, "Health", "2026-09-12", "Pharmacy"),
            (user_id, 15.00, "Entertainment", "2026-09-15", "Movie ticket"),
            (user_id, 60.00, "Shopping", "2026-09-18", "New t-shirt"),
            (user_id, 10.00, "Other", "2026-09-20", "Miscellaneous"),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            sample_expenses
        )
