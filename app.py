from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_demo_only"  # change in production

# ================================
# GEMINI API CONFIG (SAFE WAY)
# ================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ================================
# DB SIMULATION (In-memory)
# ================================
users = {}  # username -> {password, name, email}

# ================================
# ROUTES
# ================================
@app.route("/", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    user = users.get(session['username'], {})

    # Force profile completion
    if not user.get('name'):
        return redirect(url_for('profile'))

    if request.method == "POST":
        course = request.form.get("course")
        roadmap = generate_course_roadmap(course)
        return render_template("roadmap.html", course=course, roadmap=roadmap)

    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username and password:
            session['username'] = username
            if username not in users:
                users[username] = {'password': password}
            return redirect(url_for('profile'))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    if request.method == "POST":
        users[username]['name'] = request.form.get("name")
        users[username]['email'] = request.form.get("email")
        return redirect(url_for('index'))

    return render_template("profile.html", profile=users.get(username, {}))


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ================================
# GEMINI FUNCTION
# ================================
def generate_course_roadmap(course):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        You are an expert learning mentor.
        Create a clear beginner-to-advanced learning roadmap for: {course}

        Rules:
        - Step-by-step stages
        - Short bullet points
        - Practical focus
        - Simple language
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
