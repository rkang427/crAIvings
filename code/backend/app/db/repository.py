from code.backend.app.db.connection import connect
from code.backend.app.model.restaurant import Restaurant

def fetch_restaurant():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurant")
        rows = cursor.fetchall()
        return [Restaurant(*row) for row in rows]
