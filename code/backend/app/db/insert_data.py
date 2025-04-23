import psycopg2
category_keywords = []
with open("food_categories.txt", "r") as f:
    for a in f.readlines():
        category_keywords.append(a.strip())

#derived from all_categories.txt
def create_business_db(connection, data):
    for a in data[:400]:  # Limit for testing
        categories = a.get("categories")
        if not categories:
            continue
        if any(keyword in categories for keyword in category_keywords):
            with connection.cursor() as cursor:
                print(a["name"])
                #insert_core_business(cursor, [a])
                #insert_category_business(cursor, a['business_id'], categories)
    connection.commit()

def insert_core_business(connection, data):
    template = [(a['business_id'], a['name'], a['address'],
                    a['city'], a['state'], a['postal_code'],
                    a['latitude'], a['longitude'], a['stars'],
                    a['review_count'], a['is_open']) for a in data]
    connection.executemany("INSERT INTO restaurant(id, name, address,"
                           "city, state, postal_code, latitude, longitude,"
                           "stars, review_count,"
                           " is_open ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", template)

# def insert_category_business(connection, data):
#     template = []
#     for a in data:
#         template = [(a['business_id'],a['categories']) for a in data]
#     for a in template:
#         connection.execute("INSERT INTO restaurant_categories(business_id, "
#                            "name) VALUES (%s,%s)", template)
