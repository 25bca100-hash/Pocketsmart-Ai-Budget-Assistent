import os
import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    send_from_directory
)

from dotenv import load_dotenv
from jinja2 import ChoiceLoader, FileSystemLoader


# =========================================================
# SETTINGS
# =========================================================

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)

DATABASE = os.path.join(PROJECT_DIR, "pocketsmart.db")


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_DIR, "templates"),
    static_folder=BASE_DIR,
    static_url_path="/static"
)
app.jinja_loader = ChoiceLoader([
    app.jinja_loader,
    FileSystemLoader(PROJECT_DIR)
])
app.secret_key = os.getenv("SECRET_KEY") or "pocketsmart-secret-key-2026"


# =========================================================
# DATABASE
# =========================================================

def get_db():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def init_db():

    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            budget REAL NOT NULL,
            recommendation TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# Create database automatically
init_db()


# =========================================================
# HOME / LOGIN
# =========================================================

@app.route("/")
def index():

    if "username" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "").strip()

        if not username or not password:

            return render_template(
                "register.html",
                error="Please enter username and password."
            )

        connection = get_db()

        try:

            connection.execute(
                """
                INSERT INTO users (username, password)
                VALUES (?, ?)
                """,
                (username, password)
            )

            connection.commit()

            connection.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "register.html",
                error="Username already exists."
            )


    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        password = request.form.get("password", "").strip()

        connection = get_db()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username, password)
        ).fetchone()

        connection.close()

        if user:

            session["username"] = username

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password."
        )


    return render_template("login.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "username" not in session:

        return redirect(url_for("login"))
    
    if request.method == "POST":
        return redirect(url_for("dashboard"))

    username = session["username"]
    connection = get_db()
    total_budget = connection.execute(
        """
        SELECT COALESCE(SUM(budget), 0) AS total_budget
        FROM history
        WHERE username = ?
        """,
        (username,)
    ).fetchone()["total_budget"]
    category_totals = connection.execute(
        """
        SELECT category, SUM(budget) AS total_budget
        FROM history
        WHERE username = ?
        GROUP BY category
        ORDER BY total_budget DESC
        """,
        (username,)
    ).fetchall()
    connection.close()

    largest_category_total = max(
        (row["total_budget"] for row in category_totals),
        default=0
    )
    budget_breakdown = [
        {
            "category": row["category"],
            "total_budget": row["total_budget"],
            "bar_width": round(row["total_budget"] / largest_category_total * 100)
            if largest_category_total > 0 else 0
        }
        for row in category_totals
    ]

    return render_template(
        "dashboard.html",
        username=username,
        total_budget=total_budget,
        budget_breakdown=budget_breakdown
    )


# =========================================================
# HOME PLANNER
# =========================================================

@app.route("/home", methods=["GET", "POST"])
def home_planner():

    if "username" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        budget = request.form.get("budget", "0")

        details = request.form.get(
            "details",
            request.form.get("requirements", "")
        )

        try:

            budget = float(budget)

        except ValueError:

            budget = 0


        recommendation = create_recommendation(
            "Home Interior",
            budget,
            details
        )


        save_history(
            session["username"],
            "Home Interior",
            budget,
            recommendation
        )


        return render_template(
            "recommendation.html",
            recommendation=recommendation,
            category="Home Interior",
            budget=budget
        )


    return render_template("home_planner.html")


# =========================================================
# PARTY PLANNER
# =========================================================

@app.route("/party", methods=["GET", "POST"])
def party_planner():

    if "username" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        budget = request.form.get("budget", "0")

        details = request.form.get(
            "details",
            request.form.get("requirements", "")
        )

        try:

            budget = float(budget)

        except ValueError:

            budget = 0


        recommendation = create_recommendation(
            "Party Planning",
            budget,
            details
        )


        save_history(
            session["username"],
            "Party Planning",
            budget,
            recommendation
        )


        return render_template(
            "recommendation.html",
            recommendation=recommendation,
            category="Party Planning",
            budget=budget
        )


    return render_template("party_planner.html")


# =========================================================
# JEWELRY PLANNER
# =========================================================

@app.route("/jewelry", methods=["GET", "POST"])
def jewelry_planner():

    if "username" not in session:

        return redirect(url_for("login"))

    if request.method == "POST":

        budget = request.form.get("budget", "0")

        details = request.form.get(
            "details",
            request.form.get("requirements", "")
        )

        try:

            budget = float(budget)

        except ValueError:

            budget = 0


        recommendation = create_recommendation(
            "Jewelry",
            budget,
            details
        )


        save_history(
            session["username"],
            "Jewelry",
            budget,
            recommendation
        )


        return render_template(
            "recommendation.html",
            recommendation=recommendation,
            category="Jewelry",
            budget=budget
        )


    return render_template("jewelry_planner.html")


# =========================================================
# RECOMMENDATION PAGE
# =========================================================

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():

    if "username" not in session:

        return redirect(url_for("login"))


    if request.method == "POST":

        category = request.form.get(
            "category",
            "General Planning"
        )

        budget = request.form.get(
            "budget",
            "0"
        )

        details = request.form.get(
            "details",
            request.form.get(
                "requirements",
                ""
            )
        )


        try:

            budget = float(budget)

        except ValueError:

            budget = 0


        result = create_recommendation(
            category,
            budget,
            details
        )


        save_history(
            session["username"],
            category,
            budget,
            result
        )


        return render_template(
            "recommendation.html",
            recommendation=result,
            category=category,
            budget=budget
        )


    return render_template(
        "recommendation.html",
        recommendation="Enter your requirements to generate a recommendation."
    )


# =========================================================
# CREATE RECOMMENDATION
# =========================================================

def create_recommendation(
    category,
    budget,
    details
):

    # Try Gemini if available
    try:
        try:
            from google import genai as google_genai
            use_new_sdk = True
        except ImportError:
            import google.generativeai as google_genai
            use_new_sdk = False

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key:
            prompt = f"""
You are PocketSmart AI.

Planner:
{category}

Budget:
₹{budget}

User requirements:
{details}

Give a practical budget-friendly recommendation.

Include:
1. Suggested items
2. Approximate cost
3. Budget allocation
4. Estimated total
5. Money-saving suggestions

Keep the answer simple and useful.
"""

            if use_new_sdk:
                client = google_genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                text = getattr(response, "text", None)
                if text:
                    return text
            else:
                google_genai.configure(api_key=api_key)
                model = google_genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                text = getattr(response, "text", None)
                if text:
                    return text
                candidates = getattr(response, "candidates", None)
                if candidates:
                    parts = getattr(candidates[0].content, "parts", [])
                    if parts:
                        combined = "".join(
                            getattr(part, "text", "")
                            for part in parts
                            if hasattr(part, "text")
                        )
                        if combined:
                            return combined

    except Exception as error:

        print(
            "Gemini unavailable:",
            error
        )


    # =====================================================
    # FALLBACK RESULT
    # =====================================================

    main_amount = budget * 0.60

    supporting_amount = budget * 0.20

    extra_amount = budget * 0.10

    reserve_amount = budget * 0.10


    return f"""
POCKETSMART AI RECOMMENDATION

Category:
{category}

Budget:
₹{budget:,.2f}

Your Requirements:
{details}

Suggested Budget Plan:

1. Main items
   ₹{main_amount:,.2f}

2. Supporting items
   ₹{supporting_amount:,.2f}

3. Accessories / Decoration
   ₹{extra_amount:,.2f}

4. Emergency / Extra Budget
   ₹{reserve_amount:,.2f}

Estimated Total:
₹{budget:,.2f}

Money Saving Tip:
Compare different options before purchasing and keep
a small amount of your budget as emergency money.

PocketSmart AI has created this basic recommendation.
"""


# =========================================================
# SAVE HISTORY
# =========================================================

def save_history(
    username,
    category,
    budget,
    recommendation
):

    connection = get_db()

    connection.execute(
        """
        INSERT INTO history
        (
            username,
            category,
            budget,
            recommendation
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            category,
            budget,
            recommendation
        )
    )

    connection.commit()

    connection.close()


# =========================================================
# HISTORY
# =========================================================

@app.route("/history", methods=["GET", "POST"])
def history():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        return redirect(url_for("history"))

    connection = get_db()

    records = connection.execute(
        """
        SELECT *
        FROM history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (session["username"],)
    ).fetchall()

    connection.close()

    return render_template(
        "history.html",
        history=records
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# JAVASCRIPT FILE
# =========================================================

@app.route("/script.js")
def script():

    return send_from_directory(
        PROJECT_DIR,
        "script.js"
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       PocketSmart AI")
    print("======================================")
    print()
    print("Server starting...")
    print()
    print("Open this in your browser:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )