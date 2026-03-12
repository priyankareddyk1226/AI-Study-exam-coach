import sqlite3

# This creates student.db automatically
conn = sqlite3.connect("student.db")

cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")

# WEAK TOPICS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS weak_topics(
topic TEXT,
accuracy REAL
)
""")

# STUDY PLAN TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS study_plan(
day INTEGER,
topic TEXT,
material TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")