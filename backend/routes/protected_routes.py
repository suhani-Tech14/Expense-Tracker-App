from flask import Blueprint, jsonify, request
from utils.auth_middleware import login_required

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    return jsonify({
        "message": "Access granted",
        "user_id": request.user_id
    })
