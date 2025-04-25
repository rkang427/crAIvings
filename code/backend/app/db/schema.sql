--\i /Users/rheekang/docker_projects/crAIvings/code/backend/app/db/schema/schema.sql

-- write above to create


-- db_craivings=> \dt
-- : Schema |             Name              | Type  |     Owner
-- --------+-------------------------------+-------+----------------
--  public | restaurant                    | table | craivings_user
--  public | restaurant_ambience           | table | craivings_user
--  public | restaurant_attributes         | table | craivings_user
--  public | restaurant_best_nights        | table | craivings_user
--  public | restaurant_categories         | table | craivings_user
--  public | restaurant_dietary            | table | craivings_user
--  public | restaurant_dynamic_attributes | table | craivings_user
--  public | restaurant_good_for_meal      | table | craivings_user
--  public | restaurant_hours              | table | craivings_user
--  public | restaurant_music              | table | craivings_user
--  public | restaurant_parking            | table | craivings_user

DROP TABLE IF EXISTS restaurant CASCADE;
DROP TABLE IF EXISTS restaurant_attributes CASCADE;
DROP TABLE IF EXISTS restaurant_hours CASCADE;
DROP TABLE IF EXISTS restaurant_categories CASCADE;
DROP TABLE IF EXISTS restaurant_ambience CASCADE;
DROP TABLE IF EXISTS restaurant_parking CASCADE;
DROP TABLE IF EXISTS restaurant_good_for_meal CASCADE;
DROP TABLE IF EXISTS restaurant_dynamic_attributes CASCADE;
DROP TABLE IF EXISTS restaurant_best_nights CASCADE;
DROP TABLE IF EXISTS restaurant_music CASCADE;
DROP TABLE IF EXISTS restaurant_dietary CASCADE;

CREATE TABLE restaurant(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    stars FLOAT NOT NULL,
    review_count INT NOT NULL,
    is_open TEXT NOT NULL
);

CREATE TABLE restaurant_categories (
    business_id TEXT REFERENCES restaurant(id),
    category TEXT,
    PRIMARY KEY (business_id, category)
);

CREATE TABLE restaurant_hours (
    business_id TEXT REFERENCES restaurant(id),
    day_of_week TEXT,
    open_time TIME,
    close_time TIME,
    PRIMARY KEY (business_id, day_of_week)
);

CREATE TABLE restaurant_attributes(
    business_id TEXT PRIMARY KEY REFERENCES restaurant(id),
    by_appointment_only BOOLEAN,
    accept_credit_cards BOOLEAN,
    restaurant_price_range TEXT,
    coat_check BOOLEAN,
    take_out BOOLEAN,
    delivery BOOLEAN,
    caters BOOLEAN,
    wifi TEXT,
    wheelchair BOOLEAN,
    happy_hour BOOLEAN,
    outdoor_seating BOOLEAN,
    tv BOOLEAN,
    reservation BOOLEAN,
    dogs_allowed BOOLEAN,
    alcohol TEXT,
    good_for_kids BOOLEAN,
    restaurants_attire TEXT,
    restaurant_table_service BOOLEAN,
    drive_thru BOOLEAN,
    noise_level TEXT,
    accepts_bitcoin BOOLEAN,
    smoking BOOLEAN,
    good_for_dancing BOOLEAN,
    accepts_insurance BOOLEAN,
    best_nights TEXT,
    byob BOOLEAN,
    corkage BOOLEAN,
    byob_corkage BOOLEAN,
    open_24_hours BOOLEAN,
    restaurant_counter_services BOOLEAN,
    ages_allowed TEXT
);

CREATE TABLE restaurant_best_nights(
    business_id TEXT REFERENCES restaurant(id),
    day_of_week TEXT,
    PRIMARY KEY (business_id, day_of_week)
);

CREATE TABLE restaurant_music(
    business_id TEXT REFERENCES restaurant(id),
    music TEXT,
    PRIMARY KEY (business_id, music)
);

CREATE TABLE restaurant_dietary(
    business_id TEXT REFERENCES restaurant(id),
    dietary TEXT,
    PRIMARY KEY (business_id, dietary)
);

CREATE TABLE restaurant_parking (
    business_id TEXT REFERENCES restaurant(id),
    parking_type TEXT,
    PRIMARY KEY (business_id, parking_type)
);

CREATE TABLE restaurant_ambience (
    business_id TEXT REFERENCES restaurant(id),
    vibe TEXT,
    PRIMARY KEY (business_id, vibe)
);

CREATE TABLE restaurant_good_for_meal (
    business_id TEXT REFERENCES restaurant(id),
    occasion TEXT,
    PRIMARY KEY (business_id, occasion)
);

CREATE TABLE restaurant_dynamic_attributes (
    business_id TEXT REFERENCES restaurant(id),
    attribute_key TEXT,
    attribute_value JSONB,
    PRIMARY KEY (business_id, attribute_key)
);

