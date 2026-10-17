from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_db_connection

savings = Blueprint("savings", __name__)


@savings.route("/savings", methods=["POST"])
@jwt_required()
def add_saving():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    amount = data.get("amount")
    saving_date = data.get("saving_date")

    if not amount:
        return jsonify({
            "message": "Amount is required"
        }), 400

    connection = None

    try:
        connection = get_db_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                saving_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            INSERT INTO savings (user_id, amount, saving_date)
            VALUES (?, ?, ?)
        """, (user_id, amount, saving_date))

        connection.commit()

        return jsonify({
            "message": "Savings added successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@savings.route("/savings", methods=["GET"])
@jwt_required()
def get_savings():
    user_id = get_jwt_identity()
    connection = None

    try:
        connection = get_db_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                saving_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        records = connection.execute("""
            SELECT id, amount, saving_date, created_at
            FROM savings
            WHERE user_id = ?
            ORDER BY saving_date DESC
        """, (user_id,)).fetchall()

        return jsonify({
            "user_id": user_id,
            "savings": [dict(row) for row in records]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()