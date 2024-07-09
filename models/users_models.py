import matplotlib.pyplot as plt
import pandas as pd
from models.config import connection
import json

def get_user_id_by_name(username):
    conn = connection()
    with conn.cursor() as cursor:
        query = "SELECT user_id FROM Users WHERE username = ?;"
        cursor.execute(query, (username,))
        res = cursor.fetchone()
        return res[0] if res else None

def get_all_users():
    conn = connection()
    with conn.cursor() as cursor:
        query = "SELECT * FROM Users;"
        cursor.execute(query)
        res = cursor.fetchall()

        users_list = []
        for user in res:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
            }
            users_list.append(user_dict)

        return json.dumps(users_list)

def is_valid_user(username, password):
    conn = connection()
    with conn.cursor() as cursor:
        query = "SELECT * FROM Users WHERE username = ? AND password = ?;"
        cursor.execute(query, (username, password))
        res = cursor.fetchone()
        return res is not None

def add_user(username, password, email):
    conn = connection()
    with conn.cursor() as cursor:
        query = "INSERT INTO Users (username, password, email) VALUES (?, ?, ?);"
        cursor.execute(query, (username, password, email))
        conn.commit()

def generate_annual_expense_graph(user_id):
    conn = connection()
    with conn.cursor() as cursor:
        query = """
        SELECT date, amount 
        FROM Expenses 
        WHERE user_id = ?
        """
        cursor.execute(query, (user_id,))
        rows = cursor.fetchall()

    if not rows:
        raise ValueError("No expense data found for the user")

    dates = [row[0] for row in rows]
    amounts = [float(row[1]) for row in rows]  # Convert decimal to float

    if not amounts:
        raise ValueError("No numeric data to plot")

    df = pd.DataFrame({'date': dates, 'amount': amounts})
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    annual_expenses = df.groupby('year')['amount'].sum()

    if annual_expenses.empty:
        raise ValueError("No numeric data to plot")

    plt.figure(figsize=(10, 5))
    annual_expenses.plot(kind='bar', color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Total Expenses')
    plt.title(f'Annual Expenses for User {user_id}')

    graph_path = f'static/images/annual_expense_graph_{user_id}.png'
    plt.savefig(graph_path)
    plt.close()

    return graph_path
