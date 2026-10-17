from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_db_connection

loans = Blueprint("loans", __name__)


@loans.route("/loans", methods=["POST"])
@jwt_required()
def add_loan():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    loan_name = data.get("loan_name")
    principal_amount = data.get("principal_amount")
    emi = data.get("emi")
    interest_rate = data.get("interest_rate", 0)

    if not loan_name or not principal_amount or not emi:
        return jsonify({
            "message": "Loan name, principal amount and EMI are required"
        }), 400

    connection = None

    try:
        connection = get_db_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                loan_name TEXT NOT NULL,
                principal_amount REAL NOT NULL,
                emi REAL NOT NULL,
                interest_rate REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        connection.execute("""
            INSERT INTO loans
            (user_id, loan_name, principal_amount, emi, interest_rate)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            loan_name,
            principal_amount,
            emi,
            interest_rate
        ))

        connection.commit()

        return jsonify({
            "message": "Loan added successfully"
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@loans.route("/loans", methods=["GET"])
@jwt_required()
def get_loans():
    user_id = get_jwt_identity()
    connection = None

    try:
        connection = get_db_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                loan_name TEXT NOT NULL,
                principal_amount REAL NOT NULL,
                emi REAL NOT NULL,
                interest_rate REAL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        records = connection.execute("""
            SELECT id, loan_name, principal_amount,
                   emi, interest_rate, created_at
            FROM loans
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,)).fetchall()

        return jsonify({
            "user_id": user_id,
            "loans": [dict(row) for row in records]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()