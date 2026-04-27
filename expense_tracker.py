# ==========================================
# SMART EXPENSE TRACKER PRO
# Upgraded with:
# 1. Update Expense
# 2. Category Summary
# 3. Charts
# 4. Budget Alert
# 5. AI Prediction
# ==========================================

import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# ------------------------------------------
# Database Connection
# ------------------------------------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    note TEXT
)
""")

conn.commit()

# ------------------------------------------
# Add Expense
# ------------------------------------------
def add_expense():
    amount = float(input("Enter Amount: ₹"))
    category = input("Enter Category: ")
    note = input("Enter Note: ")
    date = input("Enter Date (DD-MM-YYYY) or Enter for today: ")

    if date == "":
        date = datetime.today().strftime("%d-%m-%Y")

    cursor.execute(
        "INSERT INTO expenses(amount, category, date, note) VALUES (?, ?, ?, ?)",
        (amount, category, date, note)
    )

    conn.commit()
    print("Expense Added!\n")


# ------------------------------------------
# View Expenses
# ------------------------------------------
def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    print("\nID | Amount | Category | Date | Note")
    print("-" * 60)

    for row in rows:
        print(row)

    print()


# ------------------------------------------
# Total Expense
# ------------------------------------------
def total_expense():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"Total Expense = ₹{total}\n")


# ------------------------------------------
# Delete Expense
# ------------------------------------------
def delete_expense():
    expense_id = input("Enter ID to Delete: ")

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    print("Deleted Successfully!\n")


# ------------------------------------------
# Update Expense
# ------------------------------------------
def update_expense():
    expense_id = input("Enter Expense ID to Update: ")
    amount = float(input("Enter New Amount: ₹"))
    category = input("Enter New Category: ")
    note = input("Enter New Note: ")

    cursor.execute("""
    UPDATE expenses
    SET amount=?, category=?, note=?
    WHERE id=?
    """, (amount, category, note, expense_id))

    conn.commit()
    print("Expense Updated!\n")


# ------------------------------------------
# Search Category
# ------------------------------------------
def search_category():
    category = input("Enter Category: ")

    cursor.execute(
        "SELECT * FROM expenses WHERE category LIKE ?",
        ('%' + category + '%',)
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print()


# ------------------------------------------
# Monthly Report
# ------------------------------------------
def monthly_report():
    month = input("Enter Month (MM): ")

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE substr(date,4,2)=?",
        (month,)
    )

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"Total Expense in Month {month}: ₹{total}\n")


# ------------------------------------------
# Category Summary
# ------------------------------------------
def category_summary():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    rows = cursor.fetchall()

    print("Category Wise Summary:")
    for row in rows:
        print(f"{row[0]} : ₹{row[1]}")

    print()


# ------------------------------------------
# Pie Chart
# ------------------------------------------
def show_chart():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    rows = cursor.fetchall()

    categories = []
    amounts = []

    for row in rows:
        categories.append(row[0])
        amounts.append(row[1])

    if amounts:
        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expense Distribution")
        plt.show()
    else:
        print("No Data Available!\n")


# ------------------------------------------
# Budget Alert
# ------------------------------------------
def budget_alert():
    budget = float(input("Enter Monthly Budget: ₹"))
    month = input("Enter Month (MM): ")

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE substr(date,4,2)=?",
        (month,)
    )

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print(f"Total Expense = ₹{total}")

    if total > budget:
        print("⚠ Budget Exceeded!\n")
    else:
        print("Within Budget 👍\n")


# ------------------------------------------
# AI Prediction
# ------------------------------------------
def predict_expense():
    cursor.execute("SELECT date, amount FROM expenses")
    rows = cursor.fetchall()

    monthly_data = {}

    for row in rows:
        month = int(row[0].split("-")[1])
        monthly_data[month] = monthly_data.get(month, 0) + row[1]

    if len(monthly_data) < 2:
        print("Need at least 2 months data!\n")
        return

    months = np.array(list(monthly_data.keys())).reshape(-1, 1)
    totals = np.array(list(monthly_data.values()))

    model = LinearRegression()
    model.fit(months, totals)

    next_month = max(monthly_data.keys()) + 1
    prediction = model.predict([[next_month]])

    print(f"Predicted Expense for Month {next_month}: ₹{prediction[0]:.2f}\n")


# ------------------------------------------
# Main Menu
# ------------------------------------------
while True:
    print("===== SMART EXPENSE TRACKER PRO =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Delete Expense")
    print("5. Update Expense")
    print("6. Search Category")
    print("7. Monthly Report")
    print("8. Category Summary")
    print("9. Show Pie Chart")
    print("10. Budget Alert")
    print("11. AI Expense Prediction")
    print("12. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        total_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        update_expense()
    elif choice == "6":
        search_category()
    elif choice == "7":
        monthly_report()
    elif choice == "8":
        category_summary()
    elif choice == "9":
        show_chart()
    elif choice == "10":
        budget_alert()
    elif choice == "11":
        predict_expense()
    elif choice == "12":
        print("Thank You!")
        break
    else:
        print("Invalid Choice!\n")

conn.close()