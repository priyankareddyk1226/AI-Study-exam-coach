import sqlite3
from material import materials

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Get weak topics
cursor.execute("SELECT topic FROM weak_topics")
topics = cursor.fetchall()

day = 1

for topic in topics:

    topic_name = topic[0]

    cursor.execute(
        "INSERT INTO study_plan VALUES (?,?,?)",
        (
            day,
            topic_name,
            materials.get(topic_name, "Search Google")
        )
    )

    day += 1

conn.commit()
conn.close()

print("✅ Study plan created successfully!")