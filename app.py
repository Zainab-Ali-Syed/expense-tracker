from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import init_db, seed_db, create_user, get_user_by_email, get_user_by_id
from database.queries import get_user_by_id as get_profile_by_id, get_recent_transactions, get_category_breakdown, get_summary_stats
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-12345")

@app.context_processor
def inject_user():
    """
    Makes the current logged-in user available in all templates.
    """
    user_id = session.get("user_id")
    if user_id:
        return {"current_user": get_user_by_id(user_id)}
    return {"current_user": None}


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_pw = generate_password_hash(password)

        try:
            create_user(name, email, hashed_pw)
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Email already registered")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = get_user_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            return redirect(url_for("landing"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_id = session.get("user_id")
    user_profile = get_profile_by_id(user_id)

    if not user_profile:
        abort(404)

    summary_stats = get_summary_stats(user_id)
    summary_stats = {
        "total_spent": f"₹{summary_stats['total_spent']:.2f}",
        "transaction_count": summary_stats['transaction_count'],
        "top_category": summary_stats['top_category']
    }

    recent_transactions = [
        {
            **tx,
            "amount": f"₹{tx['amount']:.2f}",
            "badge_class": f"badge-{tx['category'].lower()}"
        }
        for tx in get_recent_transactions(user_id)
    ]

    category_data = get_category_breakdown(user_id)

    color_map = {
        "Housing": "color-blue",
        "Shopping": "color-purple",
        "Dining": "color-orange",
        "Transport": "color-green"
    }

    category_breakdown = [
        {
            **item,
            "amount": f"₹{item['amount']:.2f}",
            "color_class": color_map.get(item['category'], "color-gray")
        }
        for item in category_data
    ]

    return render_template(
        "profile.html",
        user_profile=user_profile,
        summary_stats=summary_stats,
        recent_transactions=recent_transactions,
        category_breakdown=category_breakdown
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
