from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from helpers import get_db_connection, login_required

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    user_id = session.get("user_id")
    # Fetch all cards (after potential insertion)
    cards = []
    if user_id:
        with get_db_connection() as conn:
            cards = conn.execute(
                "SELECT * FROM cards WHERE user_id = ? ORDER BY id DESC",
                (user_id,)
            ).fetchall()

    return render_template("index.html", cards=cards)


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Please fill in both fields."

        hash_pw = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_pw))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists."
        finally:
            conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with get_db_connection() as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user is None or not check_password_hash(user["hash"], password):
            return "Invalid username or password."

        # Save user_id in session
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("index", ))

    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user_id = session["user_id"]

    # Fetch username from the database
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT username FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if user is None:
            return redirect(url_for("login"))

        if request.method == "POST":
            front = request.form.get("front")
            back = request.form.get("back")

            if not front or not back:
                return "Please fill in both sides of the card."

            # Insert new card
            conn.execute(
                "INSERT INTO cards (user_id, front, back) VALUES (?, ?, ?)",
                (user_id, front, back)
            )
            conn.commit()

        # Fetch all cards (after potential insertion)
        cards = conn.execute(
            "SELECT * FROM cards WHERE user_id = ? ORDER BY id DESC",
            (user_id,)
        ).fetchall()

    return render_template("dashboard.html", cards=cards, username=user["username"])


@app.route("/study", methods=["GET", "POST"])
@login_required
def study():
    with get_db_connection() as conn:
        cards = conn.execute(
            "SELECT * FROM cards WHERE user_id = ? AND learned = 0",
            (session["user_id"],)
        ).fetchall()

    # If user has no cards yet
    if not cards:
        return render_template("study.html", card=None)

    import random

    seen = session.get("seen_cards", [])
    available_cards = [c for c in cards if c["id"] not in seen]

    # If all cards were seen, reset the cycle
    if not available_cards:
        session["seen_cards"] = []
        available_cards = cards
        seen = []

    card = random.choice(available_cards)

    seen.append(card["id"])
    session["seen_cards"] = seen

    return render_template("study.html", card=card, remaining=len(available_cards) - 1)


@app.route("/mark_learned/<int:card_id>", methods=["POST"])
@login_required
def mark_learned(card_id):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE cards SET learned = 1 WHERE id = ? AND user_id = ?",
            (card_id, session["user_id"])
        )
        conn.commit()
    return redirect(url_for("study"))


if __name__ == "__main__":
    app.run(debug=True)