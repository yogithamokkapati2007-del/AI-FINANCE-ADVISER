import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv

from auth import auth
from income import income
from expenses import expenses
from savings import savings
from loans import loans
from goals import goals
from analysis import analysis
from recommendations import recommendations


load_dotenv()

app = Flask(__name__)

# Allow frontend to communicate with backend
CORS(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Register API modules
app.register_blueprint(auth, url_prefix="/api")
app.register_blueprint(income, url_prefix="/api")
app.register_blueprint(expenses, url_prefix="/api")
app.register_blueprint(savings, url_prefix="/api")
app.register_blueprint(loans, url_prefix="/api")
app.register_blueprint(goals, url_prefix="/api")
app.register_blueprint(analysis, url_prefix="/api")
app.register_blueprint(recommendations, url_prefix="/api")


@app.route("/")
def home():
    return "AI Finance Advisor Backend is Running!"


@app.route("/api/test")
def test():
    return {"message": "Backend API is working"}


@app.route("/api/status")
def status():
    return {
        "backend": "online",
        "authentication": "JWT enabled",
        "database": "MySQL configured"
    }


@app.route("/api/protected")
@jwt_required()
def protected():
    user_id = get_jwt_identity()

    return {
        "message": "You are authenticated",
        "user_id": user_id
    }


if __name__ == "__main__":
    app.run(debug=True)