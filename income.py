from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_db_connection

income = Blueprint("income", __name__)


@income.route("/income", methods=["POST"])
@jwt_required()
def add_income():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    amount = data.get("amount")
    source = data.get("source")
    income_date = data.get("income_date")

    if not amount:
        return jsonify({
            "message": "Amount is required"
        }), 400

    connection = None

    try:
        connection = get_db_connection()

        connection.execute(
            """
            INSERT INTO income (user_id, amount, source, income_date)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, amount, source, income_date)
        )

        connection.commit()

        return jsonify({
            "message": "Income added successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@income.route("/income", methods=["GET"])
@jwt_required()
def get_income():
    user_id = get_jwt_identity()
    connection = None

    try:
        connection = get_db_connection()

        records = connection.execute(
            """
            SELECT id, amount, source, income_date, created_at
            FROM income
            WHERE user_id = ?
            ORDER BY income_date DESC
            """,
            (user_id,)
        ).fetchall()

        income_records = [dict(row) for row in records]

        return jsonify({
            "user_id": user_id,
            "income": income_records
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()