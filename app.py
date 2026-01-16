from flask import Flask, render_template, request
import google.generativeai as genai

app = Flask(__name__)

# ================================
# ✅ GEMINI API CONFIG
# ================================
# Replace with your actual API key
GEMINI_API_KEY = "AIzaSyCGJ2nil0OnPLwWvS9y2LbDtTyrNsvzrdM" 
genai.configure(api_key=GEMINI_API_KEY)

# UPDATED: Use a current 2026 stable model
MODEL_NAME = "gemini-2.5-flash" 

# ================================
# ROUTES
# ================================
@app.route("/", methods=["GET", "POST"])
def index():
    roadmap = None
    course = None

    if request.method == "POST":
        course = request.form.get("course")
        roadmap = generate_course_roadmap(course)
        # Render the roadmap page only after a POST request
        return render_template("roadmap.html", course=course, roadmap=roadmap)

    # Initial load: show the selection form
    return render_template("index.html")

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