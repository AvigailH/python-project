import datetime
from flask import Flask, send_file, request, render_template, redirect, url_for, session
from models import users_models, expenses_model, category_model

app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = 'your123456789'

# הגדרת תיקיית ההעלאות
app.config['UPLOAD_FOLDER'] = 'static/images'

# דף הבית
@app.route('/')
def home():
    return render_template('index.html')

# מסלול לקבלת כל המשתמשים
@app.route('/getAllUsers')
def get_all_users():
    return users_models.get_all_users()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return render_template('register.html', error="Missing required fields")

        try:
            users_models.add_user(username, password, email)
            return redirect(url_for('home'))
        except Exception as e:
            return render_template('register.html', error=str(e))
    return render_template('register.html')

# פונקציית התחברות (לאימות המשתמש)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        if not users_models.is_valid_user(username, password):
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

        session['user_id'] = users_models.get_user_id_by_name(username)
        session['username'] = username
        session['password'] = password
        return redirect(url_for('add_expense'))

    # Handle GET request by rendering the login form
    return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     error = None
#     username = request.form['username']
#     password = request.form['password']
#
#     if not users_models.is_valid_user(username, password):
#         error = 'Invalid username or password'
#         return render_template('index.html', error=error)
#
#     session['user_id'] = users_models.get_UserId_by_name(username)
#     return redirect(url_for('add_expense'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/addExpense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        amount = data.get('amount')
        date = data.get('date')
        category_id = data.get('category_id')
        description = data.get('description')

        if not user_id or not amount or not date or not category_id:
            return "Missing required fields", 400

        try:
            expenses_model.add_expense(user_id, amount, date, category_id, description)
            return "Expense added successfully", 201
        except Exception as e:
            return str(e), 500
    else:
        categories = category_model.get_all_categories()
        return render_template('add_expense.html', categories=categories)

# מסלול ליצירת גרף ההוצאות השנתי של משתמש מסוים
@app.route('/annualExpenseGraph/<int:user_id>')
def annual_expense_graph(user_id):
    try:
        graph_path = users_models.generate_annual_expense_graph(user_id)
        return send_file(graph_path, mimetype='image/png')
    except Exception as e:
        return str(e), 500

@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return "Missing username, password or email", 400

    try:
        users_models.add_user(username, password, email)
        return "User added successfully", 201
    except Exception as e:
        return str(e), 500


@app.route('/viewExpenses', methods=['GET', 'POST'])
def view_expenses():
    expenses = []

    if request.method == 'POST':
        username = session.get('username')
        password = session.get('password')
        # username = request.form['username']
        # password = request.form['password']
        expenses = expenses_model.get_user_expenses(username, password)
        if expenses is None:
            return "User not found or invalid credentials", 403

    return render_template('view_expenses.html', expenses=expenses)


@app.route('/searchExpenses', methods=['GET', 'POST'])
def search_expenses():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        search_param = request.form['search_param']
        search_value = request.form['search_value']
        expenses = expenses_model.search_expenses_by_param(username, password, search_param, search_value)
        if expenses is None:
            return "User not found or invalid credentials", 403

        return render_template('view_expenses.html', expenses=expenses)
    else:
        return render_template('search_expenses.html')


port_number = 3000

if __name__ == '__main__':
    app.run(port=port_number)
