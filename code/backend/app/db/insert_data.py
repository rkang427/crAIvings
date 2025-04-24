import json
import ast
from datetime import datetime
from rapidfuzz import fuzz
category_keywords = []
MATCH_THRESHOLD = 50
with open("categories/food_categories.txt", "r") as f:
    for a in f.readlines():
        category_keywords.append(a.strip().lower())


def create_business_db(connection, data):
    for a in data:
        categories = [a.get("categories")]
        if not categories or categories[0] is None:
            continue
        categories = [a.lower() for a in categories]
        category_keywords_normalized = [keyword.strip().lower() for keyword in category_keywords]
        if any(fuzz.ratio(keyword, category) >= MATCH_THRESHOLD for category in categories for keyword in category_keywords_normalized):
            with connection.cursor() as cursor:
                insert_core_business(cursor, [a])
                insert_category_business(cursor, a['business_id'], categories)
                insert_attributes_business(cursor, a['business_id'], a['attributes'])
                insert_parking_data(cursor, a['business_id'], a)
                insert_ambience_data(cursor, a['business_id'], a)
                insert_best_nights(cursor, a['business_id'], a)
                insert_good_for_meal(cursor, a['business_id'], a)
                insert_hours_data(cursor, a['business_id'], a)
                insert_music_data(cursor, a['business_id'], a)
                insert_dietary(cursor, a['business_id'], a)
                insert_dynamic_attributes(cursor, a['business_id'], a.get("attributes"))
    connection.commit()
    #TODO: maybe change is_open into a Open/Closed VARCHAR type
def insert_core_business(cursor, data):
    template = [(a['business_id'], a['name'], a['address'],
                    a['city'], a['state'], a['postal_code'],
                    a['latitude'], a['longitude'], a['stars'],
                    a['review_count'], 'open' if a['is_open'] == 1 or a['is_open'] == True else 'closed') for a in data]
    cursor.executemany("INSERT INTO restaurant(id, name, address,"
                           "city, state, postal_code, latitude, longitude,"
                           "stars, review_count,"
                           " is_open ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", template)

def insert_category_business(cursor, business_id, categories):
    if isinstance(categories, str):
        categories = [category.strip() for category in categories.split(",")]
    else:
        categories = [category.strip() for category in categories[0].split(",")]
    template = [(business_id, category) for category in categories]
    cursor.executemany("""
        INSERT INTO restaurant_categories(business_id, category)
        VALUES (%s, %s)
    """, template)

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

def insert_attributes_business(cursor, business_id, data):
    if not data or data == "None" or data == "[]":
        return
    template = (
        business_id,
        str_to_bool(data.get('ByAppointmentOnly')),
        str_to_bool(data.get('BusinessAcceptsCreditCards')),
        str_to_str(data.get('RestaurantsPriceRange2')),
        str_to_bool(data.get('CoatCheck')),
        str_to_bool(data.get('RestaurantsTakeOut')),
        str_to_bool(data.get('RestaurantsDelivery')),
        str_to_bool(data.get('Caters')),
        str_to_str(data.get('WiFi')),
        str_to_bool(data.get('WheelchairAccessible')),
        str_to_bool(data.get('HappyHour')),
        str_to_bool(data.get('OutdoorSeating')),
        str_to_bool(data.get('HasTV')),
        str_to_bool(data.get('RestaurantsReservations')),
        str_to_bool(data.get('DogsAllowed')),
        str_to_str(data.get('Alcohol')),
        str_to_bool(data.get('GoodForKids')),
        str_to_str(data.get('RestaurantsAttire')),
        str_to_bool(data.get('RestaurantsTableService')),
        str_to_bool(data.get('DriveThru')),
        str_to_str(data.get('NoiseLevel')),
        str_to_bool(data.get('BusinessAcceptsBitcoin')),
        str_to_bool(data.get('Smoking')),
        str_to_bool(data.get('GoodForDancing')),
        str_to_bool(data.get('AcceptsInsurance')),
        str_to_bool(data.get('BYOB')),
        str_to_bool(data.get('Corkage')),
        str_to_bool(data.get('BYOBCorkage')),
        str_to_str(data.get('HairSpecializesIn')),
        str_to_bool(data.get('Open24Hours')),
        str_to_bool(data.get('RestaurantsCounterService')),
        str_to_str(data.get('AgesAllowed'))
    )
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
                                          byob, corkage, byob_corkage, hair_specializes_in,
                                          open_24_hours, restaurant_counter_services, ages_allowed
                                          )
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        return "Error in parking: {e}", e

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
    for day, time_range in hours.items():
        open_time, close_time = parse_hours(time_range)
        if open_time and close_time:
            template.append((business_id, day, open_time, close_time))
    if template:
        cursor.executemany("""
            INSERT INTO restaurant_hours(business_id, day_of_week, open_time, close_time)
            VALUES (%s, %s, %s, %s)
        """, template)

def insert_good_for_meal(cursor, business_id, data):
    attributes = data.get("attributes")
    if not attributes or attributes == "None":
        return
    meals = attributes.get("GoodForMeal")
    if not meals or meals == "None":
        return
    meals = ast.literal_eval(meals) if isinstance(meals, str) else meals
    template = [(business_id, meal) for meal, is_true in meals.items() if is_true]
    if template:
        cursor.executemany("""
                INSERT INTO restaurant_good_for_meal(business_id, occasion)
                VALUES (%s, %s)
            """, template)

def insert_dietary(cursor, business_id, data):
    attributes = data.get("attributes")
    if not attributes or attributes == "None":
        return
    dietary = attributes.get("DietaryRestrictions")

    if not dietary or dietary == "None":
        return
    diet = ast.literal_eval(dietary) if isinstance(dietary, str) else dietary
    template = [(business_id, d) for d, is_true in diet.items() if is_true == True]
    cursor.executemany("""
                    INSERT INTO restaurant_dietary(business_id, dietary)
                    VALUES (%s, %s)
                """, template)

def insert_dynamic_attributes(cursor, business_id, attributes):
    if not attributes or attributes == "None":
        return
    template = [
        (business_id, key, json.dumps(ast.literal_eval(value) if isinstance(value, str) else value))
        for key, value in attributes.items()
    ]
    cursor.executemany("""
        INSERT INTO restaurant_dynamic_attributes(business_id, attribute_key, attribute_value)
        VALUES (%s, %s, %s)
    """, template)
