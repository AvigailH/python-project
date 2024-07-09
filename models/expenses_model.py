from models.config import connection

def get_user_expenses(username, password):
    conn = connection()
    with conn.cursor() as cursor:
        user_query = "SELECT user_id FROM Users WHERE username = ? AND password = ?;"
        cursor.execute(user_query, (username, password))
        user = cursor.fetchone()
        if not user:
            return None
        user_id = user[0]

        query = "SELECT e.*, c.category_name FROM Expenses e JOIN Categories c ON e.category_id = c.category_id WHERE e.user_id = ?;"
        cursor.execute(query, (user_id,))
        res = cursor.fetchall()
        return res

def search_expenses_by_param(username, password, search_param, search_value):
    conn = connection()
    with conn.cursor() as cursor:
        user_query = "SELECT user_id FROM Users WHERE username = ? AND password = ?;"
        cursor.execute(user_query, (username, password))
        user = cursor.fetchone()
        if not user:
            return None

        user_id = user[0]

        query = f"SELECT e.*, c.category_name FROM Expenses e JOIN Categories c ON e.category_id = c.category_id WHERE e.user_id = ? AND {search_param} LIKE ?;"
        cursor.execute(query, (user_id, f"%{search_value}%"))
        res = cursor.fetchall()
        return res

def add_expense(user_id, amount, date, category_id, description):
    conn = connection()
    with conn.cursor() as cursor:
        query = "INSERT INTO Expenses (user_id, amount, date, category_id, description) VALUES (?, ?, ?, ?, ?);"
        cursor.execute(query, (user_id, amount, date, category_id, description))
        conn.commit()


def update_expense(expense_id, user_id=None, amount=None, category=None, date=None, description=None):
    conn = connection()
    with conn.cursor() as cursor:
        updates = []
        params = []
        if user_id:
            updates.append("user_id = ?")
            params.append(user_id)
        if amount:
            updates.append("amount = ?")
            params.append(amount)
        if category:
            updates.append("category = ?")
            params.append(category)
        if date:
            updates.append("date = ?")
            params.append(date)
        if description:
            updates.append("description = ?")
            params.append(description)
        params.append(expense_id)
        query = f"UPDATE Expenses SET {', '.join(updates)} WHERE expense_id = ?;"
        cursor.execute(query, tuple(params))
        conn.commit()

def delete_expense(expense_id):
    conn = connection()
    with conn.cursor() as cursor:
        query = "DELETE FROM Expenses WHERE expense_id = ?;"
        cursor.execute(query, (expense_id,))
        conn.commit()
