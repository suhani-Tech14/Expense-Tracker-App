from database.db import get_db_connection
from services.email_service import send_email


def send_monthly_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all users
    cursor.execute("SELECT id, email FROM users")
    users = cursor.fetchall()

    for user in users:
        user_id = user["id"]
        email = user["email"]

        # Get monthly expenses grouped by category
        cursor.execute("""
            SELECT category_id, SUM(amount) AS total
            FROM expenses
            WHERE user_id = ?
            AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
            GROUP BY category_id
        """, (user_id,))

        rows = cursor.fetchall()

        if not rows:
            continue

        body = "Your Monthly Expense Summary\n\n"
        grand_total = 0

        for row in rows:
            body += f"Category {row['category_id']}: ₹{row['total']}\n"
            grand_total += row["total"]

        body += f"\nTotal Spent: ₹{grand_total}"

        send_email(
            to_email=email,
            subject="Your Monthly Expense Summary",
            body=body
        )

    conn.close()
