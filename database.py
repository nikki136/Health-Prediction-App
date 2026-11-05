import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "patients.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT NOT NULL,
                glucose REAL NOT NULL,
                haemoglobin REAL NOT NULL,
                cholesterol REAL NOT NULL,
                remarks TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

def get_all_patients():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM patients ORDER BY id ASC").fetchall()

def get_patient(patient_id):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()

def create_patient(data, remarks):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO patients
            (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data["full_name"], data["date_of_birth"], data["email"], data["glucose"],
              data["haemoglobin"], data["cholesterol"], remarks))

def update_patient(patient_id, data, remarks):
    with get_connection() as conn:
        conn.execute("""
            UPDATE patients
            SET full_name=?, date_of_birth=?, email=?, glucose=?, haemoglobin=?,
                cholesterol=?, remarks=?
            WHERE id=?
        """, (data["full_name"], data["date_of_birth"], data["email"], data["glucose"],
              data["haemoglobin"], data["cholesterol"], remarks, patient_id))

def delete_patient(patient_id):
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        return cursor.rowcount > 0
