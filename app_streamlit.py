import streamlit as st
import pandas as pd
import mysql.connector

# DB connection
conn = mysql.connector.connect(
    host="localhost",
    user="tracker_user",
    password="1234",
    database="expense_tracker"
)

st.title("💸 Expense Tracker (Python + SQL)")

# Add expense form
st.subheader("Add Expense")

date = st.date_input("Date")
category = st.text_input("Category")
amount = st.number_input("Amount")

if st.button("Add Expense"):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, category, amount) VALUES (%s, %s, %s)",
        (date, category, amount)
    )
    conn.commit()
    st.success("Expense added!")

# Load data
df = pd.read_sql("SELECT * FROM expenses", conn)

if not df.empty:
    st.subheader("All Expenses")
    st.dataframe(df)

    # Category summary
    st.subheader("Category-wise Spending")
    category_summary = df.groupby('category')['amount'].sum()
    st.bar_chart(category_summary)

    # Monthly trend
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    monthly = df.groupby('month')['amount'].sum()

    st.subheader("Monthly Trend")
    st.line_chart(monthly)

conn.close()