import ast
import json
from datetime import datetime
from rapidfuzz import fuzz
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORY_FILE_PATH = os.path.join(BASE_DIR, "categories", "food_categories.txt")

category_keywords = []
MATCH_THRESHOLD = 50
with open(CATEGORY_FILE_PATH, "r") as f:
    for line in f.readlines():
        category_keywords.append(line.strip().lower())

def str_to_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, str):
        val = val.strip().lower()
        return val in ['true', 't', 'yes', 'y', '1']
    return False

def str_to_str(val):
    if val is None:
        return None
    try:
        return ast.literal_eval(val) if isinstance(val, str) else val
    except (ValueError, SyntaxError):
        return val

from rapidfuzz import process

def get_matching_category(categories, threshold=50):
    for category in categories:
        match = process.extractOne(category, category_keywords, score_cutoff=threshold)
        if match:
            return True
    return False

def create_business_db(connection, data):
    #data = data[:1000]
    try:
        with connection.cursor() as cursor:
            for business in data:
                categories = [business.get("categories")]
                if not categories or categories[0] is None:
                    continue

                categories = [a.lower() for a in categories]
                if get_matching_category(categories):
                    insert_core_business(cursor, [business])
                    insert_category_business(cursor, business['business_id'], categories)
                    insert_attributes_business(cursor, business['business_id'], business['attributes'])
                    insert_parking_data(cursor, business['business_id'], business)
                    insert_ambience_data(cursor, business['business_id'], business)
                    insert_best_nights(cursor, business['business_id'], business)
                    insert_good_for_meal(cursor, business['business_id'], business)
                    insert_hours_data(cursor, business['business_id'], business)
                    insert_music_data(cursor, business['business_id'], business)
                    insert_dietary(cursor, business['business_id'], business)
                    insert_dynamic_attributes(cursor, business['business_id'], business.get("attributes"))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.rollback()


def insert_core_business(cursor, data):

    template = [
        (business['business_id'],
         business['name'],
         business['address'],
         business['city'],
         business['state'],
         business['postal_code'],
         business['latitude'],
         business['longitude'],
         business['stars'],
         business['review_count'],
         'open' if business['is_open'] == 1 else 'closed')
        for business in data
    ]
    print(template)


    cursor.executemany("""
        INSERT INTO restaurant(id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, template)

def insert_category_business(cursor, business_id, categories):
    if isinstance(categories, str):
        categories = [category.strip() for category in categories.split(",")]
    else:
        categories = [category.strip() for category in categories[0].split(",")]
    template = [(business_id, category) for category in categories]

    cursor.executemany("""
        INSERT INTO restaurant_categories(business_id, category)
        VALUES (%s, %s)
        ON CONFLICT (business_id, category) DO NOTHING
    """, template)

def insert_attributes_business(cursor, business_id, data):
    if not data or data == "None" or data == "[]":
        return
    if data.get('HairSpecializesIn') is not None:
        return
    template = (
        business_id,
        bool(data.get('ByAppointmentOnly')),
        bool(data.get('BusinessAcceptsCreditCards')),
        bool(data.get('RestaurantsPriceRange2')),
        bool(data.get('CoatCheck')),
        bool(data.get('RestaurantsTakeOut')),
        bool(data.get('RestaurantsDelivery')),
        bool(data.get('Caters')),
        data.get('WiFi'),
        bool(data.get('WheelchairAccessible')),
        bool(data.get('HappyHour')),
        bool(data.get('OutdoorSeating')),
        bool(data.get('HasTV')),
        bool(data.get('RestaurantsReservations')),
        bool(data.get('DogsAllowed')),
        data.get('Alcohol'),
        bool(data.get('GoodForKids')),
        data.get('RestaurantsAttire'),
        bool(data.get('RestaurantsTableService')),
        bool(data.get('DriveThru')),
        data.get('NoiseLevel'),
        bool(data.get('BusinessAcceptsBitcoin')),
        bool(data.get('Smoking')),
        bool(data.get('GoodForDancing')),
        bool(data.get('AcceptsInsurance')),
        bool(data.get('BYOB')),
        bool(data.get('Corkage')),
        bool(data.get('BYOBCorkage')),
        bool(data.get('Open24Hours')),
        bool(data.get('RestaurantsCounterService')),
        data.get('AgesAllowed')
    )
    print(template)
    cursor.executemany("""
        INSERT INTO restaurant_attributes(business_id,
                                          by_appointment_only, accept_credit_cards,
                                          restaurant_price_range, coat_check, take_out, delivery,
                                          caters, wifi, wheelchair,
                                          happy_hour, outdoor_seating, tv, reservation, dogs_allowed,
                                          alcohol, good_for_kids, restaurants_attire,
                                          restaurant_table_service, drive_thru, noise_level,
                                          accepts_bitcoin, smoking,
                                          good_for_dancing, accepts_insurance,
                                          byob, corkage, byob_corkage,
                                          open_24_hours, restaurant_counter_services, ages_allowed
                                          )
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [template])


def insert_ambience_data(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    ambience_data = data["attributes"].get("Ambience")
    if not ambience_data or ambience_data == "None":
        return
    pk = ast.literal_eval(ambience_data) if isinstance(ambience_data, str) else ambience_data
    if isinstance(pk, dict):
        template = [
            (business_id, ambience)
            for ambience, is_true in pk.items() if is_true == True
        ]
        cursor.executemany("""
        INSERT INTO restaurant_ambience(business_id, vibe)
        VALUES (%s, %s)
    """, template)

def insert_music_data(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    music_data = data["attributes"].get("Music")
    if not music_data or music_data == "None":
        return
    pk = ast.literal_eval(music_data) if isinstance(music_data, str) else music_data
    if isinstance(pk, dict):
        template = [
            (business_id, music)
            for music, is_true in pk.items() if is_true
        ]
        cursor.executemany("""
            INSERT INTO restaurant_music(business_id, music)
            VALUES (%s, %s)
        """, template)

def insert_parking_data(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    parking = data["attributes"].get("BusinessParking")
    if not parking or parking == "None":
        return
    try:
        pk = ast.literal_eval(parking) if isinstance(parking, str) else parking
        template = [
                (business_id, parking_type)
                for parking_type, is_true in pk.items() if is_true == True
        ]
        cursor.executemany("""
                INSERT INTO restaurant_parking(business_id, parking_type)
                VALUES (%s, %s)
            """, template)
        bike = data["attributes"].get("BikeParking")
        if bike and bike == "True":
            cursor.execute("""
                INSERT INTO restaurant_parking(business_id, parking_type)
                VALUES (%s, 'bike')
            """, (business_id,))
    except Exception as e:
        return f"Error in parking: {e}", e

def insert_best_nights(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    best_nights = data["attributes"].get("BestNights")
    if not best_nights or best_nights == "None":
        return
    pk = ast.literal_eval(best_nights) if isinstance(best_nights, str) else best_nights
    if isinstance(pk, dict):
        template = [
            (business_id, day)
            for day, is_true in pk.items() if is_true == True
        ]
        cursor.executemany("""
            INSERT INTO restaurant_best_nights(business_id, day_of_week)
            VALUES (%s, %s)
        """, template)

def parse_hours(hours_str):
    try:
        open_time_str, close_time_str = hours_str.split("-")
        open_time = datetime.strptime(open_time_str.strip().zfill(5), "%H:%M").time()
        close_time = datetime.strptime(close_time_str.strip().zfill(5), "%H:%M").time()
        return open_time, close_time
    except:
        return None, None

def insert_hours_data(cursor, business_id, data):
    hours = data.get("hours")
    if not hours:
        return
    template = []
    for day, times in hours.items():
        open_time, close_time = parse_hours(times)
        if open_time and close_time:
            template.append((business_id, day, open_time, close_time))
    cursor.executemany("""
        INSERT INTO restaurant_hours(business_id, day_of_week, open_time, close_time)
        VALUES (%s, %s, %s, %s)
    """, template)

def insert_dynamic_attributes(cursor, business_id, attributes):
    if not attributes or attributes == "None":
        return
    template = []
    if isinstance(attributes, str):
        attributes = ast.literal_eval(attributes)
    for attribute, value in attributes.items():
        if isinstance(value, bool):
            template.append((business_id, attribute, value))
    cursor.executemany("""
        INSERT INTO restaurant_dynamic_attributes(business_id, attribute, value)
        VALUES (%s, %s, %s)
    """, template)

def insert_good_for_meal(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    good_for_meal = data["attributes"].get("GoodForMeal")
    if not good_for_meal or good_for_meal == "None":
        return
    pk = ast.literal_eval(good_for_meal) if isinstance(good_for_meal, str) else good_for_meal
    if isinstance(pk, dict):
        template = [
            (business_id, meal)
            for meal, is_true in pk.items() if is_true
        ]
        cursor.executemany("""
            INSERT INTO restaurant_good_for_meal(business_id, occasion)
            VALUES (%s, %s)
        """, template)

def insert_dietary(cursor, business_id, data):
    if not data["attributes"] or data["attributes"] == "None":
        return
    dietary = data["attributes"].get("DietaryRestrictions")
    if not dietary or dietary == "None":
        return
    pk = ast.literal_eval(dietary) if isinstance(dietary, str) else dietary
    if isinstance(pk, dict):
        template = [
            (business_id, restriction)
            for restriction, is_true in pk.items() if is_true
        ]
        cursor.executemany("""
            INSERT INTO restaurant_dietary(business_id, dietary)
            VALUES (%s, %s)
        """, template)
