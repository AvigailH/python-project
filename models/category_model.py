from models.config import connection
def get_all_categories():
    conn = connection()
    with conn.cursor() as cursor:
        query = "SELECT * FROM Categories;"
        cursor.execute(query)
        res = cursor.fetchall()
        return res

def add_category(name):
    conn = connection()
    with conn.cursor() as cursor:
        query = "INSERT INTO Categories (name) VALUES (?);"
        cursor.execute(query, (name,))
        conn.commit()


def update_category(category_id, name):
    conn = connection()
    with conn.cursor() as cursor:
        query = "UPDATE Categories SET name = ? WHERE category_id = ?;"
        cursor.execute(query, (name, category_id))
        conn.commit()

def delete_category(category_id):
    conn = connection()
    with conn.cursor() as cursor:
        query = "DELETE FROM Categories WHERE category_id = ?;"
        cursor.execute(query, (category_id,))
        conn.commit()
