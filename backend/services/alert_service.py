from database.db import get_db_connection
from services.email_service import send_email


def check_monthly_limit(user_id, user_email):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user's monthly limit
    cursor.execute(
        "SELECT monthly_limit FROM users WHERE id = ?",
        (user_id,)
    )
    limit_row = cursor.fetchone()
    monthly_limit = limit_row["monthly_limit"]

    # Calculate current month total
    cursor.execute(
        """
        SELECT SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        AND strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
        """,
        (user_id,)
    )
    result = cursor.fetchone()
    total = result["total"] if result["total"] else 0

    conn.close()

    # Send alert if exceeded
    if total > monthly_limit:
        send_email(
            to_email=user_email,
            subject="Expense Alert: Monthly Limit Exceeded",
            body=(
                f"Your monthly expenses are ₹{total}.\n"
                f"Your set limit is ₹{monthly_limit}.\n\n"
                "Please review your spending."
            )
        )
