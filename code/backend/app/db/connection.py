import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect():
    try:
        url = os.getenv("DATABASE_URL")
        print("Connecting to:", url)
        connection = psycopg2.connect(url)
        print("connection worked!")
        return connection
    except Exception as e:
        print("connection failed due to ", e)
        return None

def connect_local():
    try:
        connection = psycopg2.connect(
            dbname="db_craivings",
            user="craivings_user",
            password="password",
            host="localhost",
            port="5432",
            connect_timeout=10
        )
        return connection
    except Exception as e:
        print("Unable to connect to database: {}".format(e))
        return None