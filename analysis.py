from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

analysis = Blueprint("analysis", __name__)


def calculate_financial_metrics(total_income, total_expenses, debt_payments):
    monthly_savings = total_income - total_expenses - debt_payments

    savings_rate = (
        (monthly_savings / total_income) * 100
        if total_income > 0 else 0
    )

    expense_ratio = (
        (total_expenses / total_income) * 100
        if total_income > 0 else 0
    )

    dti = (
        (debt_payments / total_income) * 100
        if total_income > 0 else 0
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "debt_payments": debt_payments,
        "monthly_savings": monthly_savings,
        "savings_rate": round(savings_rate, 2),
        "expense_ratio": round(expense_ratio, 2),
        "dti": round(dti, 2)
    }


def classify_financial_health(savings_rate, dti, expense_ratio):
    if savings_rate >= 20 and dti <= 30 and expense_ratio <= 70:
        return "Healthy"

    if savings_rate >= 10 and dti <= 40 and expense_ratio <= 85:
        return "Moderate"

    return "Needs Improvement"


@analysis.route("/analysis/test", methods=["GET"])
def test_analysis():
    metrics = calculate_financial_metrics(50000, 30000, 5000)

    health = classify_financial_health(
        metrics["savings_rate"],
        metrics["dti"],
        metrics["expense_ratio"]
    )

    return jsonify({
        "message": "Financial analysis working",
        "analysis": metrics,
        "financial_health": health
    }), 200


@analysis.route("/analysis/calculate", methods=["POST"])
@jwt_required()
def calculate_analysis():
    user_id = get_jwt_identity()
    data = request.get_json()

    total_income = float(data.get("total_income", 0))
    total_expenses = float(data.get("total_expenses", 0))
    debt_payments = float(data.get("debt_payments", 0))

    metrics = calculate_financial_metrics(
        total_income,
        total_expenses,
        debt_payments
    )

    health = classify_financial_health(
        metrics["savings_rate"],
        metrics["dti"],
        metrics["expense_ratio"]
    )

    return jsonify({
        "message": "Financial analysis calculated",
        "user_id": user_id,
        "analysis": metrics,
        "financial_health": health
    }), 200


@analysis.route("/analysis", methods=["GET"])
@jwt_required()
def financial_analysis():
    user_id = get_jwt_identity()

    return jsonify({
        "message": "Financial analysis endpoint working",
        "user_id": user_id,
        "analysis": {
            "total_income": 0,
            "total_expenses": 0,
            "monthly_savings": 0,
            "savings_rate": 0,
            "expense_ratio": 0,
            "dti": 0
        }
    }), 200