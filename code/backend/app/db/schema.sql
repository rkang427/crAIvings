--\i /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/schema.sql
-- write above the first time to create


-- db_craivings=> \dt
--                         List of relations
--  Schema |             Name              | Type  |     Owner
-- --------+-------------------------------+-------+----------------
--  public | restaurant                    | table | craivings_user
--  public | restaurant_ambience           | table | craivings_user
--  public | restaurant_attributes         | table | craivings_user
--  public | restaurant_best_nights        | table | craivings_user
--  public | restaurant_categories         | table | craivings_user
--  public | restaurant_dynamic_attributes | table | craivings_user


--in case pre-existing
DROP TABLE IF EXISTS restaurant_attributes CASCADE;
DROP TABLE IF EXISTS restaurant_hours CASCADE;
DROP TABLE IF EXISTS restaurant_categories CASCADE;
DROP TABLE IF EXISTS restaurant CASCADE;
DROP TABLE IF EXISTS restaurant_ambience CASCADE;
DROP TABLE IF EXISTS restaurant_parking CASCADE;
DROP TABLE IF EXISTS restaurant_good_for_meal CASCADE;
DROP TABLE IF EXISTS restaurant_dynamic_attributes CASCADE;
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
    is_open INTEGER NOT NULL
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
    business_id VARCHAR PRIMARY KEY REFERENCES restaurant(id),
    by_appointment_only BOOLEAN,
    accept_credit_cards BOOLEAN,
    bike_parking BOOLEAN,
    restaurant_price_range VARCHAR,
    coat_check BOOLEAN,
    take_out BOOLEAN,
    delivery BOOLEAN,
    caters BOOLEAN,
    wifi VARCHAR,
    wheelchair BOOLEAN,
    happy_hour BOOLEAN,
    outdoor_seating BOOLEAN,
    tv BOOLEAN,
    reservation BOOLEAN,
    dogs_allowed BOOLEAN,
    alcohol VARCHAR,
    good_for_kids BOOLEAN,
    restaurants_attire VARCHAR,
    restaurant_table_service BOOLEAN,
    drive_thru BOOLEAN,
    noise_level VARCHAR,
    good_for_meal VARCHAR,
    accepts_bitcoin BOOLEAN,
    smoking BOOLEAN,
    music BOOLEAN,
    good_for_dancing BOOLEAN,
    accepts_insurance BOOLEAN,
    best_nights VARCHAR,
    byob BOOLEAN,
    corkage BOOLEAN,
    byob_corkage BOOLEAN,
    hair_specializes_in VARCHAR,
    open_24_hours BOOLEAN,
    restaurant_counter_services BOOLEAN,
    ages_allowed VARCHAR,
    dietary_restrictions VARCHAR,
    dynamic_attributes JSONB
);

CREATE TABLE restaurant_best_nights(
    business_id VARCHAR REFERENCES restaurant(id),
    day_of_week VARCHAR,
    PRIMARY KEY (business_id, day_of_week)
);

CREATE TABLE restaurant_parking (
    business_id VARCHAR REFERENCES restaurant(id),
    parking_type VARCHAR,
    available BOOLEAN,
    PRIMARY KEY (business_id, parking_type)
);

CREATE TABLE restaurant_ambience (
    business_id VARCHAR REFERENCES restaurant(id),
    vibe VARCHAR,
    PRIMARY KEY (business_id, vibe)
);


CREATE TABLE restaurant_good_for_meal (
    business_id VARCHAR REFERENCES restaurant(id),
    occasion VARCHAR,
    PRIMARY KEY (business_id, occasion)
);

CREATE TABLE restaurant_dynamic_attributes (
    business_id VARCHAR REFERENCES restaurant(id),
    attribute_key VARCHAR,
    attribute_value JSONB,
    PRIMARY KEY (business_id, attribute_key)
);
