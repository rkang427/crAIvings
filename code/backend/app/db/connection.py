import psycopg2
from psycopg2 import sql

def connect():
    try:
        connection = psycopg2.connect(
            dbname="db_craivings",
            user="craivings_user",
            password="password",
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print("Unable to connect to database: {}".format(e))
        return None