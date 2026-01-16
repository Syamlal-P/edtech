from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super-secret-key"   # change later

# -------------------------
# HOME
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# AUTH
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role")   # student / teacher / expert

        # Temporary session-based login (hackathon safe)
        session["user"] = username
        session["role"] = role

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# -------------------------
# DASHBOARD (ROLE BASED)
# -------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    role = session.get("role")

    if role == "student":
        return render_template("dashboard.html", role="Student")

    elif role == "teacher":
        return render_template("dashboard.html", role="Teacher")

    elif role == "expert":
        return render_template("dashboard.html", role="Expert")

    return redirect(url_for("logout"))


# -------------------------
# STUDENT FEATURES
# -------------------------
@app.route("/assessment")
def assessment():
    if session.get("role") != "student":
        return redirect(url_for("dashboard"))

    return render_template("assessment.html")


@app.route("/roadmap")
def roadmap():
    if session.get("role") != "student":
        return redirect(url_for("dashboard"))

    # Placeholder personalized roadmap
    skills = ["Python Basics", "Problem Solving", "Data Structures"]
    return render_template("roadmap.html", skills=skills)


# -------------------------
# TEACHER / EXPERT ANALYTICS
# -------------------------
@app.route("/analytics")
def analytics():
    if session.get("role") not in ["teacher", "expert"]:
        return redirect(url_for("dashboard"))

    return render_template("analytics.html")


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
