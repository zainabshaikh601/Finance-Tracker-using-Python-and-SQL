# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import sqlite3

# Create a SQLite database and table
conn = sqlite3.connect('finance_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        Date DATE,
        Category TEXT,
        Amount REAL
    )
''')
conn.commit()

# Predefined categories
categories = ['Food', 'Transportation', 'Housing', 'Entertainment', 'Other']

# Streamlit web app
st.title('Finance Tracker')

# Input form for adding expenses
date = st.date_input('Date', pd.to_datetime('today'))
category = st.selectbox('Category', categories)
amount = st.number_input('Amount', value=0.0)

if st.button('Add Expense'):
    # Insert the new expense into the SQLite database
    cursor.execute('INSERT INTO expenses (Date, Category, Amount) VALUES (?, ?, ?)', (date, category, amount))
    conn.commit()
    st.success('Expense added successfully!')

# Button to clear the table
if st.button('Clear Table'):
    # Clear the table in the SQLite database
    cursor.execute('DELETE FROM expenses')
    conn.commit()
    st.warning('Table cleared. All data deleted.')

# Retrieve finance data from the SQLite database
finance_data = pd.read_sql('SELECT * FROM expenses', conn)

# Display the finance data
st.subheader('Finance Data')
st.dataframe(finance_data)

# Line graph for day-wise expenses
st.subheader('Day-wise Expenses')
daywise_expenses = finance_data.groupby('Date')['Amount'].sum()
fig, ax = plt.subplots()
ax.plot(daywise_expenses.index, daywise_expenses.values, marker='o', linestyle='-')
ax.set(xlabel='Date', ylabel='Total Expense',
       title='Day-wise Expenses')
ax.grid(True)
st.pyplot(fig)

# Visualization
st.subheader('Expense Distribution by Category')
category_expenses = finance_data.groupby('Category')['Amount'].sum()
fig, ax = plt.subplots()
ax.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
st.pyplot(fig)

# Save the finance data to a CSV file (optional)
finance_data.to_csv('finance_data.csv', index=False)

# Close the SQLite connection
conn.close()
