from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_db_connection

expenses = Blueprint("expenses", __name__)


@expenses.route("/expenses", methods=["POST"])
@jwt_required()
def add_expense():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    amount = data.get("amount")
    category = data.get("category")
    description = data.get("description")
    expense_date = data.get("expense_date")

    if not amount or not category:
        return jsonify({
            "message": "Amount and category are required"
        }), 400

    connection = None

    try:
        connection = get_db_connection()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        connection.execute(
            """
            INSERT INTO expenses
            (user_id, amount, category, description, expense_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, description, expense_date)
        )

        connection.commit()

        return jsonify({
            "message": "Expense added successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@expenses.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    connection = None

    try:
        connection = get_db_connection()

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        records = connection.execute(
            """
            SELECT id, amount, category, description,
                   expense_date, created_at
            FROM expenses
            WHERE user_id = ?
            ORDER BY expense_date DESC
            """,
            (user_id,)
        ).fetchall()

        return jsonify({
            "user_id": user_id,
            "expenses": [dict(row) for row in records]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()