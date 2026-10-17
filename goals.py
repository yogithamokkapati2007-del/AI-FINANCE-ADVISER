from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import get_db_connection

goals = Blueprint("goals", __name__)


def ensure_goals_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_savings REAL DEFAULT 0,
            target_date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.commit()


@goals.route("/goals", methods=["POST"])
@jwt_required()
def add_goal():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    current_savings = data.get("current_savings", 0)
    target_date = data.get("target_date")

    if not goal_name or not target_amount or not target_date:
        return jsonify({
            "message": "Goal name, target amount and target date are required"
        }), 400

    connection = None

    try:
        connection = get_db_connection()
        ensure_goals_table(connection)

        cursor = connection.execute(
            """
            INSERT INTO goals
            (user_id, goal_name, target_amount, current_savings, target_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                goal_name,
                target_amount,
                current_savings,
                target_date
            )
        )

        connection.commit()

        return jsonify({
            "message": "Goal added successfully",
            "goal_id": cursor.lastrowid
        }), 201

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@goals.route("/goals", methods=["GET"])
@jwt_required()
def get_goals():
    user_id = get_jwt_identity()
    connection = None

    try:
        connection = get_db_connection()
        ensure_goals_table(connection)

        records = connection.execute(
            """
            SELECT id, goal_name, target_amount,
                   current_savings, target_date, created_at
            FROM goals
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

        return jsonify({
            "user_id": user_id,
            "goals": [dict(row) for row in records]
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Database error",
            "error": str(e)
        }), 500

    finally:
        if connection:
            connection.close()


@goals.route("/goals/advisor", methods=["POST"])
@jwt_required()
def savings_advisor():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    target_amount = float(data.get("target_amount", 0))
    current_savings = float(data.get("current_savings", 0))
    target_date = data.get("target_date")

    if target_amount <= 0 or not target_date:
        return jsonify({
            "message": "Target amount and target date are required"
        }), 400

    try:
        target = date.fromisoformat(target_date)
        today = date.today()

        days_remaining = (target - today).days
        remaining_amount = max(target_amount - current_savings, 0)

        if days_remaining <= 0:
            daily_target = remaining_amount
        else:
            daily_target = remaining_amount / days_remaining

        weekly_target = daily_target * 7

        return jsonify({
            "message": "Savings advisor calculated",
            "user_id": user_id,
            "advisor": {
                "target_amount": target_amount,
                "current_savings": current_savings,
                "remaining_amount": round(remaining_amount, 2),
                "days_remaining": days_remaining,
                "daily_savings_target": round(daily_target, 2),
                "weekly_savings_target": round(weekly_target, 2)
            }
        }), 200

    except ValueError:
        return jsonify({
            "message": "Invalid target date. Use YYYY-MM-DD."
        }), 400