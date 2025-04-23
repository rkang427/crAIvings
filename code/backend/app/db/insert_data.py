import json

import psycopg2
category_keywords = []
with open("categories/food_categories.txt", "r") as f:
    for a in f.readlines():
        category_keywords.append(a.strip())

#derived from all_categories.txt
def create_business_db(connection, data):
    for a in data:
        categories = a.get("categories")
        if not categories:
            continue
        if any(keyword in categories for keyword in category_keywords):
            with connection.cursor() as cursor:
                insert_core_business(cursor, [a])
                insert_category_business(cursor, a['business_id'], categories)
                insert_attributes_business(cursor, a['business_id'], a['attributes'])
                if a.get('BusinessParking'):
                    insert_parking_data(cursor, a['business_id'], a['BusinessParking'])
                if a.get('Ambience'):
                    insert_ambience_data(cursor, a['business_id'], a['ambience'])
                if a.get('GoodForMeal'):
                    insert_best_nights(cursor, a['business_id'], a['GoodForMeal'])
    connection.commit()

def insert_core_business(cursor, data):
    template = [(a['business_id'], a['name'], a['address'],
                    a['city'], a['state'], a['postal_code'],
                    a['latitude'], a['longitude'], a['stars'],
                    a['review_count'], a['is_open']) for a in data]
    cursor.executemany("INSERT INTO restaurant(id, name, address,"
                           "city, state, postal_code, latitude, longitude,"
                           "stars, review_count,"
                           " is_open ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", template)


def insert_category_business(cursor, business_id, categories):
    if isinstance(categories, str):
        categories = categories.split(",")
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
def str_to_varchar(val):
    if isinstance(val, str):
        return val.strip("u'").strip().lower()

def insert_attributes_business(cursor, business_id, data):
    if not data:
        return

    template = (
        business_id,
        str_to_bool(data.get('ByAppointmentOnly')),
        str_to_bool(data.get('BusinessAcceptsCreditCards')),
        str_to_bool(data.get('BikeParking')),
        data.get('RestaurantsPriceRange2'),
        str_to_bool(data.get('CoatCheck')),
        str_to_bool(data.get('RestaurantsTakeOut')),
        str_to_bool(data.get('RestaurantsDelivery')),
        str_to_bool(data.get('Caters')),
        str_to_varchar(data.get('WiFi')),
        str_to_bool(data.get('WheelchairAccessible')),
        str_to_bool(data.get('HappyHour')),
        str_to_bool(data.get('OutdoorSeating')),
        str_to_bool(data.get('HasTV')),
        str_to_bool(data.get('RestaurantsReservations')),
        str_to_bool(data.get('DogsAllowed')),
        str_to_varchar(data.get('Alcohol')),
        str_to_bool(data.get('GoodForKids')),
        str_to_varchar(data.get('RestaurantsAttire')),
        str_to_bool(data.get('RestaurantsTableService')),
        str_to_bool(data.get('DriveThru')),
        str_to_varchar(data.get('NoiseLevel')),
        str_to_bool(data.get('BusinessAcceptsBitcoin')),
        str_to_bool(data.get('Smoking')),
        str_to_bool(data.get('Music')),
        str_to_bool(data.get('GoodForDancing')),
        str_to_bool(data.get('AcceptsInsurance')),
        str_to_bool(data.get('BYOB')),
        str_to_bool(data.get('Corkage')),
        str_to_bool(data.get('BYOBCorkage')),
        str_to_varchar(data.get('HairSpecializesIn')),
        str_to_bool(data.get('Open24Hours')),
        str_to_bool(data.get('RestaurantsCounterService')),
        data.get('AgesAllowed'),
        data.get('DietaryRestrictions')
    )
    cursor.executemany("""
        INSERT INTO restaurant_attributes(business_id,
                                          by_appointment_only, accept_credit_cards, bike_parking,
                                          restaurant_price_range, coat_check, take_out, delivery,
                                          caters, wifi, wheelchair,
                                          happy_hour, outdoor_seating, tv, reservation, dogs_allowed,
                                          alcohol, good_for_kids, restaurants_attire,
                                          restaurant_table_service, drive_thru, noise_level,
                                          accepts_bitcoin, smoking, music,
                                          good_for_dancing, accepts_insurance,
                                          byob, corkage, byob_corkage, hair_specializes_in,
                                          open_24_hours, restaurant_counter_services, ages_allowed,
                                          dietary_restrictions)
        VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, [template])

def insert_parking_data(cursor, business_id, parking_data):
    if not parking_data:
        return
    template = [
        (business_id, parking_type, available)
        for parking_type, available in parking_data.items()
    ]
    cursor.executemany("""
        INSERT INTO restaurant_parking(business_id, parking_type, available)
        VALUES (%s, %s, %s)
    """, template)


def insert_best_nights(cursor, business_id, best_nights):
    if not best_nights:
        return
    nights = [(business_id, day) for day, is_true in best_nights.items() if is_true == True]
    if nights:
        cursor.executemany("""
            INSERT INTO restaurant_best_nights(business_id, day_of_week)
            VALUES (%s, %s)
        """, nights)


def insert_ambience_data(cursor, business_id, ambience_data):
    if not ambience_data:
        return
    template = [(business_id, vibe) for vibe, is_true in ambience_data.items() if is_true == True]

    cursor.executemany("""
        INSERT INTO restaurant_ambience(business_id, vibe)
        VALUES (%s, %s)
    """, template)


def insert_dynamic_attributes(cursor, business_id, attributes):
    if not attributes:
        return
    template = [
        (business_id, key, json.dumps(value))  # JSON encode the value to store in JSONB column
        for key, value in attributes.items()
    ]

    cursor.executemany("""
        INSERT INTO restaurant_dynamic_attributes(business_id, attribute_key, attribute_value)
        VALUES (%s, %s, %s)
    """, template)