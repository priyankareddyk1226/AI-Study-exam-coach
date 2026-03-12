import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Get weak topics
cursor.execute("SELECT * FROM weak_topics")
topics = cursor.fetchall()

print("\n🎓 PERSONALIZED AI COACH\n")

for topic in topics:

    print(f"""
📌 Topic: {topic[0]}
📉 Accuracy: {topic[1]:.2f}%

✅ Recommendation:
• Study this topic for 1 hour daily
• Practice at least 20 questions
• Review mistakes carefully
• Watch concept videos
""")

conn.close()