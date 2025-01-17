import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Database setup
conn = sqlite3.connect('finance.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS transactions 
             (date TEXT, category TEXT, amount REAL, type TEXT)''')
conn.commit()

# Sidebar Inputs
st.sidebar.header("Add New Transaction")
date = st.sidebar.date_input("Date")
category = st.sidebar.selectbox("Category", ["Salary", "Food", "Rent", "Investment", "Other"])
amount = st.sidebar.number_input("Amount", min_value=0.0)
type_ = st.sidebar.radio("Type", ["Income", "Expense"])
if st.sidebar.button("Add Transaction"):
    c.execute("INSERT INTO transactions (date, category, amount, type) VALUES (?, ?, ?, ?)", 
              (date, category, amount, type_))
    conn.commit()
    st.sidebar.success("Transaction Added!")

# Load Data
df = pd.read_sql("SELECT * FROM transactions", conn)

# Display Data
st.header("Transaction History")
st.dataframe(df)

# Visualization
st.header("Expense Breakdown")
expense_df = df[df["type"] == "Expense"].groupby("category")["amount"].sum()
fig, ax = plt.subplots()
ax.pie(expense_df, labels=expense_df.index, autopct="%1.1f%%")
st.pyplot(fig)

conn.close()
