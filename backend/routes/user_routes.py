from flask import Blueprint, request, jsonify
from database.db import get_db_connection
from utils.auth_middleware import login_required

user_bp = Blueprint("users", __name__)


@user_bp.route("/users/limit", methods=["PUT"])
@login_required
def update_limit():
    data = request.json
    new_limit = data.get("monthly_limit")

    if not new_limit:
        return jsonify({"error": "Monthly limit required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET monthly_limit = ? WHERE id = ?",
        (new_limit, request.user_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Monthly limit updated"}), 200
