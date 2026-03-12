import pandas as pd
import sqlite3
from ai_coach import generate_ai_plan


# ---------- LOAD CSV FILE ----------
data = pd.read_csv("mock_test.csv")   # file in same folder

# ---------- CONNECT DATABASE ----------
conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# ---------- CREATE TABLE IF NOT EXISTS ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS weak_topics(
    topic TEXT,
    accuracy REAL
)
""")

# ---------- CLEAR OLD DATA ----------
cursor.execute("DELETE FROM weak_topics")

# ---------- ANALYSIS ----------
result = data.groupby("topic")["correct"].mean()

weak_topics = []

for topic, accuracy in result.items():

    accuracy_percent = accuracy * 100

    if accuracy_percent < 60:

        weak_topics.append(topic)

        cursor.execute(
            "INSERT INTO weak_topics VALUES (?,?)",
            (topic, accuracy_percent)
        )

conn.commit()
conn.close()

# ---------- OUTPUT ----------
print("✅ Weak topics identified:")
print(weak_topics)