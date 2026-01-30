from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# 🔐 Secret key
app.config["SECRET_KEY"] = "super-secret-key"

# 🌍 Enable CORS
CORS(app)

# 📦 Import blueprints
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp
from routes.user_routes import user_bp

# 🧩 Register blueprints (ONLY ONCE EACH)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(protected_bp, url_prefix="/api")
app.register_blueprint(user_bp, url_prefix="/api")

from routes.expense_routes import expense_bp
app.register_blueprint(expense_bp, url_prefix="/api")


@app.route("/health")
def health():
    return {
        "status": "OK",
        "message": "Expense Tracker API running"
    }

if __name__ == "__main__":
    app.run(debug=True, port=8000)
