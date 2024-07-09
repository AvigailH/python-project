import pyodbc

def connection():
    """
    Returns a database connection.
    """
    server = 'DESKTOP-U5FNJME\\SQLEXPRESS'  # Server name
    database = 'MyExpenses'  # Database name

    # Connection string format
    connection_string = f"""
    DRIVER={{SQL Server}};
    SERVER={server};
    DATABASE={database};
    """

    connection = pyodbc.connect(connection_string)
    return connection
