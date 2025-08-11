from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from config import Config
from models import db, Expense, Budget
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Helpers
def current_month_label():
    return datetime.now().strftime("%B %Y")

@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    # Use the latest budget for the current month if available
    current_month = current_month_label()
    budget = Budget.query.filter_by(month=current_month).order_by(Budget.created_at.desc()).first()
    categories = [e.category for e in expenses]
    amounts = [e.amount for e in expenses]
    total_spent = sum(amounts) if amounts else 0.0
    budget_amount = budget.amount if budget else None
    usage_pct = round((total_spent / budget_amount) * 100, 2) if (budget_amount and budget_amount > 0) else 0
    return render_template(
        "index.html",
        expenses=expenses,
        budget=budget,
        categories=categories,
        amounts=amounts,
        total_spent=total_spent,
        usage_pct=usage_pct
    )

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        category = request.form.get("category", "").strip()
        amount = request.form.get("amount", "")
        note = request.form.get("note", "").strip()
        if not category or amount == "":
            return "Invalid input", 400
        try:
            amount = float(amount)
        except ValueError:
            return "Amount must be a number", 400

        expense = Expense(category=category, amount=amount, note=note)
        try:
            db.session.add(expense)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return "DB error", 500
        return redirect(url_for("index"))
    return render_template("add_expense.html")

@app.route("/set-budget", methods=["GET", "POST"])
def set_budget():
    if request.method == "POST":
        amount = request.form.get("amount", "")
        month = request.form.get("month") or current_month_label()
        if amount == "":
            return "Invalid input", 400
        try:
            amount = float(amount)
        except ValueError:
            return "Amount must be a number", 400

        budget = Budget(amount=amount, month=month)
        try:
            db.session.add(budget)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return "DB error", 500
        return redirect(url_for("index"))
    return render_template("set_budget.html", datetime=datetime)

@app.route("/reports")
def reports():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("reports.html", expenses=expenses)

# === JSON APIs used by AJAX ===
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def api_delete_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    try:
        db.session.delete(exp)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"ok": False, "error": "DB error"}), 500
    return jsonify({"ok": True, "id": expense_id})

@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
def api_update_expense(expense_id):
    exp = Expense.query.get_or_404(expense_id)
    data = request.get_json() or {}
    category = data.get("category", "").strip()
    amount = data.get("amount")
    note = data.get("note", "")
    date_str = data.get("date")

    if not category or amount is None:
        return jsonify({"ok": False, "error": "Missing fields"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"ok": False, "error": "Invalid amount"}), 400

    exp.category = category
    exp.amount = amount
    exp.note = note
    if date_str:
        try:
            exp.date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            pass
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"ok": False, "error": "DB error"}), 500

    return jsonify({"ok": True, "expense": exp.to_dict()})

@app.route("/api/budget/latest", methods=["GET"])
def api_latest_budget():
    current_month = current_month_label()
    budget = Budget.query.filter_by(month=current_month).order_by(Budget.created_at.desc()).first()
    if not budget:
        return jsonify({"ok": False, "budget": None}), 200
    return jsonify({"ok": True, "budget": budget.to_dict()})

@app.route("/api/budget/<int:budget_id>", methods=["DELETE"])
def api_delete_budget(budget_id):
    b = Budget.query.get_or_404(budget_id)
    try:
        db.session.delete(b)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"ok": False, "error": "DB error"}), 500
    return jsonify({"ok": True})

@app.route("/api/expenses", methods=["POST"])
def api_create_expense():
    data = request.get_json() or {}
    category = data.get("category", "").strip()
    amount = data.get("amount")
    note = data.get("note", "")
    if not category or amount is None:
        return jsonify({"ok": False, "error": "Missing fields"}), 400
    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"ok": False, "error": "Invalid amount"}), 400

    exp = Expense(category=category, amount=amount, note=note)
    try:
        db.session.add(exp)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"ok": False, "error": "DB error"}), 500

    return jsonify({"ok": True, "expense": exp.to_dict()}), 201

if __name__ == "__main__":
    app.run(debug=True)
