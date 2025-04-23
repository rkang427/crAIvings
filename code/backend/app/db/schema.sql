CREATE TABLE restaurant(
    id VARCHAR PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR NOT NULL,
    city VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    postal_code VARCHAR NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    stars FLOAT NOT NULL,
    review_count INT NOT NULL,
    is_open BOOLEAN NOT NULL
);

CREATE TABLE restaurant_categories (
    business_id VARCHAR REFERENCES restaurant(id),
    category VARCHAR,
    PRIMARY KEY (business_id, category)
);

CREATE TABLE restaurant_hours (
    business_id VARCHAR REFERENCES restaurant(id),
    day_of_week VARCHAR,
    open_time TIME,
    close_time TIME,
    PRIMARY KEY (business_id, day_of_week)
);

CREATE TABLE restaurant_attributes(
    business_id VARCHAR REFERENCES restaurant(id),
    by_appointment_only VARCHAR,
    accept_credit_cards VARCHAR,
    bike_parking VARCHAR,
    restaurant_price_range VARCHAR,
    coat_check VARCHAR,
    take_out VARCHAR,
    delivery VARCHAR,
    caters VARCHAR,
    wifi VARCHAR,
    business_parking VARCHAR,
    wheelchair VARCHAR,
    happy_hour VARCHAR,
    outdoor_seating VARCHAR,
    tv VARCHAR,
    reservation VARCHAR,
    dogs_allowed VARCHAR,
    alcohol VARCHAR,
    good_for_kids VARCHAR,
    restaurants_attire VARCHAR,
    ambience VARCHAR,
    restaurant_table_service VARCHAR,
    drive_thru VARCHAR,
    noise_level VARCHAR,
    good_for_meal VARCHAR,
    accepts_bitcoin VARCHAR,
    smoking VARCHAR,
    music VARCHAR,
    good_for_dancing VARCHAR,
    accepts_insurance VARCHAR,
    best_nights VARCHAR,
    byob VARCHAR,
    corkage VARCHAR,
    byob_corkage VARCHAR,
    hair_specializes_in VARCHAR,
    open_24_hours VARCHAR,
    restaurant_counter_services VARCHAR,
    ages_allowed VARCHAR,
    dietary_restrictions VARCHAR,
    dynamic_attributes JSONB
)
