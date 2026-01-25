from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "super_secret_key_for_demo_only" # Change this in production!

# ================================
# ✅ GEMINI API CONFIG
# ================================
# Replace with your actual API key
GEMINI_API_KEY = "paste your api key here" 
genai.configure(api_key=GEMINI_API_KEY)

# ================================
# DB SIMULATION (In-memory)
# ================================
users = {} # username -> {password, name, email}

# UPDATED: Use a current 2026 stable model
MODEL_NAME = "gemini-2.5-flash" 

# ================================
# ROUTES
# ================================
from flask import redirect, url_for, session

@app.route("/", methods=["GET", "POST"])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = users.get(session['username'], {})
    # Force profile completion if not set
    if not user.get('name'):
         return redirect(url_for('profile'))

    roadmap = None
    course = None

    if request.method == "POST":
        course = request.form.get("course")
        roadmap = generate_course_roadmap(course)
        # Render the roadmap page only after a POST request
        return render_template("roadmap.html", course=course, roadmap=roadmap)

    # Initial load: show the selection form
    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Simple mock authentication (Accept any non-empty creds for demo)
        if username and password:
            session['username'] = username
            if username not in users:
                users[username] = {'password': password} # Create mock user on fly
            return redirect(url_for('profile'))
        else:
            return render_template("login.html", error="Invalid credentials")
            
    return render_template("login.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    username = session['username']
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        
        if username in users:
            users[username]['name'] = name
            users[username]['email'] = email
            
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
        - Use Step-by-step stages
        - Short bullet points
        - Practical focus
        - Simple language
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # This will help you see if there are other issues (like API key or Quota)
        return f"Error: {str(e)}"

if __name__ == "__main__":

    app.run(debug=True)

