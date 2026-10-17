# AI Finance Advisor - Backend API Documentation

Base URL:

http://127.0.0.1:5000/api

## Authentication

Protected endpoints require:

Authorization: Bearer <JWT_TOKEN>

---

## 1. Test Backend

GET /test

Response:

{
    "message": "Backend API is working"
}

---

## 2. Backend Status

GET /status

Response:

{
    "backend": "online",
    "authentication": "JWT enabled",
    "database": "MySQL configured"
}

---

## 3. Register

POST /register

Request:

{
    "name": "John",
    "email": "john@example.com",
    "password": "password123"
}

Response:

{
    "message": "Registration successful"
}

---

## 4. Login

POST /login

Request:

{
    "email": "john@example.com",
    "password": "password123"
}

Response:

{
    "message": "Login successful",
    "token": "<JWT_TOKEN>",
    "user": {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    }
}

---

## 5. Income

POST /income

Authorization required.

Request:

{
    "amount": 50000,
    "source": "Salary",
    "income_date": "2026-09-27"
}

GET /income

Authorization required.

---

## 6. Expenses

POST /expenses

Authorization required.

Request:

{
    "amount": 5000,
    "category": "Food",
    "description": "Monthly groceries",
    "expense_date": "2026-09-27"
}

GET /expenses

Authorization required.

---

## 7. Savings

POST /savings

Authorization required.

Request:

{
    "amount": 5000,
    "saving_date": "2026-09-27"
}

GET /savings

Authorization required.

---

## 8. Loans

POST /loans

Authorization required.

Request:

{
    "loan_name": "Education Loan",
    "principal_amount": 200000,
    "emi": 5000,
    "interest_rate": 8.5
}

GET /loans

Authorization required.

---

## 9. Goals

POST /goals

Authorization required.

Request:

{
    "goal_name": "Emergency Fund",
    "target_amount": 120000,
    "current_savings": 20000,
    "target_date": "2027-01-01"
}

GET /goals

Authorization required.

---

## 10. Savings Advisor

POST /goals/advisor

Authorization required.

Request:

{
    "target_amount": 120000,
    "current_savings": 20000,
    "target_date": "2027-01-01"
}

Response contains:

- target amount
- current savings
- remaining amount
- days remaining
- daily savings target
- weekly savings target

---

## 11. Financial Analysis

POST /analysis/calculate

Authorization required.

Request:

{
    "total_income": 50000,
    "total_expenses": 30000,
    "debt_payments": 5000
}

Response contains:

- total income
- total expenses
- debt payments
- monthly savings
- savings rate
- expense ratio
- DTI
- financial health

---

## 12. Recommendations

GET /recommendations

Authorization required.

Returns personalized financial recommendations.

---

## 13. Protected Test

GET /protected

Authorization required.

Used to verify JWT authentication.