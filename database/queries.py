from database.db import get_db
from datetime import datetime

def get_user_by_id(user_id):
    """
    Fetches a user's profile information by their ID.
    Formats created_at as 'Month YYYY'.
    """
    with get_db() as conn:
        user = conn.execute("SELECT name, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            # created_at is stored as TEXT in SQLite (datetime('now'))
            # Example format: '2026-10-02 10:00:00'
            dt = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S")
            return {
                "name": user["name"],
                "email": user["email"],
                "member_since": dt.strftime("%B %Y"),
                "initials": "".join([n[0] for n in user["name"].split()]).upper()
            }
        return None

def get_summary_stats(user_id):
    """
    Fetch total spent, transaction count, and top category for a user.
    """
    with get_db() as conn:
        # Total spent and transaction count
        stats = conn.execute(
            "SELECT SUM(amount), COUNT(id) FROM expenses WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        total_spent = stats[0] if stats[0] is not None else 0.0
        transaction_count = stats[1] if stats[1] is not None else 0

        # Top category
        top_cat_row = conn.execute(
            """
            SELECT category FROM expenses
            WHERE user_id = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()

        top_category = top_cat_row[0] if top_cat_row else "—"

        return {
            "total_spent": total_spent,
            "transaction_count": transaction_count,
            "top_category": top_category
        }

def get_recent_transactions(user_id, limit=10):
    """
    Queries the expenses table for the given user_id.
    Returns a list of dictionaries with: date, description, category, and amount.
    """
    with get_db() as conn:
        query = "SELECT date, description, category, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT ?"
        rows = conn.execute(query, (user_id, limit)).fetchall()
        return [dict(row) for row in rows]

def get_category_breakdown(user_id):
    """
    Returns total amount and percentage per category for a user.
    Ensures the sum of percentages is exactly 100.
    """
    with get_db() as conn:
        # Get total spending first
        total_row = conn.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ?", (user_id,)).fetchone()
        total_spent = total_row[0] if total_row and total_row[0] else 0

        if total_spent == 0:
            return []

        # Get spending per category
        rows = conn.execute(
            "SELECT category, SUM(amount) as amount FROM expenses WHERE user_id = ? GROUP BY category ORDER BY amount DESC",
            (user_id,)
        ).fetchall()

        breakdown = []
        total_percentage = 0

        for row in rows:
            category = row["category"]
            amount = row["amount"]
            percentage = round((amount / total_spent) * 100)
            breakdown.append({
                "category": category,
                "amount": amount,
                "percentage": percentage
            })
            total_percentage += percentage

        # Adjust the largest category to make the total exactly 100
        diff = 100 - total_percentage
        if diff != 0 and breakdown:
            # breakdown is already sorted by amount DESC, so index 0 is the largest
            breakdown[0]["percentage"] += diff

        return breakdown
