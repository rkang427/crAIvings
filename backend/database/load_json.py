# import json
# import os
# import sys
#
# import utils.backend.app.database.connection
# import utils.backend.app.database.insert_data
# from utils.backend.app.database.connection import connect
# from utils.backend.app.database.insert_data import create_business_db
#
# path_business = "../../../data/raw/yelp_dataset/yelp_academic_dataset_business.json"
# path_checkin = "../../../data/raw/yelp_dataset/yelp_academic_dataset_checkin.json"
# path_review = "../../../data/raw/yelp_dataset/yelp_academic_dataset_review.json"
# path_tip = "../../../data/raw/yelp_dataset/yelp_academic_dataset_tip.json"
# path_user = "../../../data/raw/yelp_dataset/yelp_academic_dataset_user.json"
#
#
# def load_json(file_path):
#     if not os.path.exists(file_path):
#         return None
#     with open(file_path, 'r', encoding='utf-8') as f:
#         try:
#             data = json.load(f)
#             return data
#         except json.JSONDecodeError as e:
#             print(f"Error {file_path}: {e}")
#             return None
#
#
# def load_data():
#     business = load_json(path_business)
#     checkins = load_json(path_checkin)
#     review = load_json(path_review)
#     tip = load_json(path_tip)
#     user = load_json(path_user)
#
#     return business, checkins, review, tip, user
#
#
# def insert_data_into_db(business):
#     connection = connect()
#     if connection:
#         create_business_db(connection, business)
#         connection.close()
#
#
# if __name__ == "__main__":
#     business, checkins, review, tip, user = load_data()
#     if business:
#         insert_data_into_db(business)
import json
import os

from backend.app.db.connection import connect, connect_local
from backend.app.db.insert_data import create_business_db

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
BUSINESS_JSON_PATH = os.path.join(BASE_DIR, "data", "raw", "yelp_dataset", "yelp_academic_dataset_business.json")

def load_and_insert_business_data():
    with open(BUSINESS_JSON_PATH, "r") as file:
        data = [json.loads(line) for line in file]

    connection = connect()
    if connection:
        create_business_db(connection, data)
        connection.close()
        print("done.")

if __name__ == "__main__":
    load_and_insert_business_data()
