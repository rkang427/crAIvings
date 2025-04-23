from code.backend.app.db.connection import connect
from code.backend.app.model.restaurant import Restaurant
from code.backend.app.model.restaurant_parking import Parking

def fetch_restaurant():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurant")
        rows = cursor.fetchall()
        return [Restaurant(*row) for row in rows]

def fetch_parking():
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM restaurant_parking")
        rows = cursor.fetchall()
        return [Parking(*row) for row in rows]