import sqlite3
import config

conn = sqlite3.connect(config.DATABASE)

tables = conn.execute("""
SELECT name FROM sqlite_master
WHERE type='table';
""").fetchall()

print("Tables found:", tables)

conn.close()