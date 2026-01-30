from functools import wraps
from flask import request, jsonify
from services.jwt_service import decode_token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401

        user_id = decode_token(token)

        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user_id = user_id
        return f(*args, **kwargs)

    return decorated
