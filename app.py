from flask import Flask, render_template, request, redirect, session
import pandas as pd
import sqlite3
from ai_coach import generate_ai_plan

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- STUDY MATERIAL LINKS ----------
materials = {
    "Algebra": "https://www.khanacademy.org/math/algebra",
    "Calculus": "https://www.khanacademy.org/math/calculus",
    "Mechanics": "https://www.youtube.com/results?search_query=physics+mechanics",
    "Organic": "https://www.youtube.com/results?search_query=organic+chemistry"
}

# ---------- AUTO YOUTUBE LINK ----------
def get_material_link(topic):

    if topic in materials:
        return materials[topic]

    search_query = topic.replace(" ", "+") + "+lecture"
    youtube_link = "https://www.youtube.com/results?search_query=" + search_query

    return youtube_link


# ---------- CREATE DATABASE ----------
def init_db():

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weak_topics(
        topic TEXT,
        accuracy REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_plan(
        day INTEGER,
        topic TEXT,
        material TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------- DATABASE HELPER ----------
def query_db(query, params=()):

    conn = sqlite3.connect("student.db")
    cursor = conn.cursor()

    cursor.execute(query, params)
    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data


# ---------- SIMPLE AI ADVICE ----------
def get_ai_advice(topics):

    if not topics:
        return "Great job! You don't have weak topics."

    message = "You should focus on improving: "

    for t in topics:
        message += t + ", "

    message += ". Practice these topics daily for better results."

    return message


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = query_db(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Please enter username and password"

        query_db(
            "INSERT INTO users(username, password) VALUES (?,?)",
            (username, password)
        )

        return redirect("/login")

    return render_template("register.html")


# ---------- UPLOAD MOCK TEST ----------
@app.route("/upload", methods=["POST"])
def upload():

    if "user" not in session:
        return redirect("/")

    file = request.files.get("file")

    if not file or file.filename == "":
        return redirect("/dashboard")

    # Read CSV
    data = pd.read_csv(file)

    # Normalize column names
    data.columns = data.columns.str.lower().str.strip()

    # Check topic column
    if "topic" not in data.columns:
        return "CSV must contain a 'topic' column"

    # Detect correctness column
    correct_col = None
    for col in ["correct", "is_correct", "result", "answer"]:
        if col in data.columns:
            correct_col = col
            break

    if correct_col is None:
        return "CSV must contain a correctness column (correct / result / answer)"

    data[correct_col] = pd.to_numeric(data[correct_col], errors="coerce")

    # Clear old results
    query_db("DELETE FROM weak_topics")
    query_db("DELETE FROM study_plan")

    # Accuracy per topic
    result = data.groupby("topic")[correct_col].mean()

    weak_topics = []

    # Detect weak topics
    for topic, accuracy in result.items():

        accuracy_percent = accuracy * 100

        if accuracy_percent < 60:

            weak_topics.append(topic)

            query_db(
                "INSERT INTO weak_topics VALUES (?,?)",
                (topic, accuracy_percent)
            )

    # Generate simple study plan
    ai_plan = weak_topics

    day = 1

    for topic in ai_plan:

        if day > 7:
            break

        material_link = get_material_link(topic)

        query_db(
            "INSERT INTO study_plan VALUES (?,?,?)",
            (day, topic, material_link)
        )

        day += 1

    return redirect("/dashboard")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    weak = query_db("SELECT * FROM weak_topics")
    plan = query_db("SELECT * FROM study_plan")

    advice = ""

    if weak:
        topic_names = [t[0] for t in weak]
        advice = generate_ai_plan(topic_names)

    return render_template(
        "dashboard.html",
        weak=weak,
        plan=plan,
        advice=advice,
        user=session["user"]
    )


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run(debug=True)