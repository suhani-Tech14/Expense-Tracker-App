from flask import Blueprint, request, jsonify
from database.db import get_db_connection
from utils.auth_middleware import login_required
from services.alert_service import check_monthly_limit

expense_bp = Blueprint("expenses", __name__)

# ---------------- ADD EXPENSE ----------------
@expense_bp.route("/expenses", methods=["POST"])
@login_required
def add_expense():
    data = request.json

    category_id = data.get("category_id")
    amount = data.get("amount")
    description = data.get("description", "")
    expense_date = data.get("expense_date")

    if not category_id or not amount or not expense_date:
        return jsonify({"error": "Required fields missing"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses (user_id, category_id, amount, description, expense_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        (request.user_id, category_id, amount, description, expense_date)
    )

    conn.commit()
    conn.close()

    # 🔔 EMAIL ALERT CHECK (AFTER SUCCESSFUL INSERT)
    check_monthly_limit(request.user_id, request.user_email)

    return jsonify({"message": "Expense added successfully"}), 201


# ---------------- VIEW EXPENSES ----------------
@expense_bp.route("/expenses", methods=["GET"])
@login_required
def get_expenses():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total count
    cursor.execute(
        "SELECT COUNT(*) as total FROM expenses WHERE user_id = ?",
        (request.user_id,)
    )
    total = cursor.fetchone()["total"]

    # Paginated data
    cursor.execute(
        """
        SELECT id, amount, category_id, description, expense_date
        FROM expenses
        WHERE user_id = ?
        ORDER BY expense_date DESC
        LIMIT ? OFFSET ?
        """,
        (request.user_id, limit, offset)
    )

    expenses = cursor.fetchall()
    conn.close()

    return jsonify({
        "expenses": [dict(row) for row in expenses],
        "page": page,
        "limit": limit,
        "total": total
    }), 200
