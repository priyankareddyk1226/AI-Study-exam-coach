from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def generate_ai_plan(topics):

    topic_text = ", ".join(topics)

    prompt = f"""
Create a detailed 7-day study plan for a student weak in: {topic_text}

Rules:
- Give exactly 7 days
- Each day must contain 3 or 4 study tasks
- Tasks should include studying theory, watching lectures, and practicing problems
- Keep it clear and structured

Format exactly like this:

Day 1:
- Task
- Task
- Task

Day 2:
- Task
- Task
- Task

Continue until Day 7.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content