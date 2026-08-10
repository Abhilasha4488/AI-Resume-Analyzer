import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "resume_analyzer.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# =========================
# Users Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


# =========================
# Resumes Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS resumes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    filename TEXT,
    resume_score INTEGER,
    ats_score INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")


# =========================
# Skills Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS skills(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER,
    skill TEXT,
    FOREIGN KEY(resume_id) REFERENCES resumes(id)
)
""")


# =========================
# Jobs Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_title TEXT,
    required_skills TEXT
)
""")


# =========================
# Certificates / Achievements Table
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS certificates(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    organization TEXT,
    issue_date TEXT,
    certificate_url TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")


# =========================
# Save Changes
# =========================

conn.commit()

print("Database created at:")
print(DB_PATH)

conn.close()

print("Database created successfully!")

