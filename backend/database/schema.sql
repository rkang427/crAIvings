--\i /Users/rheekang/docker_projects/crAIvings/utils/backend/pages/db/schema/schema.sql

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
CREATE EXTENSION IF NOT EXISTS plpgsql;

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
    is_open TEXT NOT NULL,
    search_vector tsvector
);

CREATE TABLE restaurant_categories (
    business_id TEXT REFERENCES restaurant(id),
    category TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, category)
);

CREATE TABLE restaurant_hours (
    business_id TEXT REFERENCES restaurant(id),
    day_of_week TEXT,
    open_time TIME,
    close_time TIME,
    search_vector tsvector,
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
    search_vector tsvector,
    ages_allowed TEXT
);

CREATE TABLE restaurant_best_nights(
    business_id TEXT REFERENCES restaurant(id),
    day_of_week TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, day_of_week)
);

CREATE TABLE restaurant_music(
    business_id TEXT REFERENCES restaurant(id),
    music TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, music)
);

CREATE TABLE restaurant_dietary(
    business_id TEXT REFERENCES restaurant(id),
    dietary TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, dietary)
);

CREATE TABLE restaurant_parking (
    business_id TEXT REFERENCES restaurant(id),
    parking_type TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, parking_type)
);

CREATE TABLE restaurant_ambience (
    business_id TEXT REFERENCES restaurant(id),
    vibe TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, vibe)
);

CREATE TABLE restaurant_good_for_meal (
    business_id TEXT REFERENCES restaurant(id),
    occasion TEXT,
    search_vector tsvector,
    PRIMARY KEY (business_id, occasion)
);

CREATE TABLE restaurant_dynamic_attributes (
    business_id TEXT REFERENCES restaurant(id),
    attribute_key TEXT,
    attribute_value JSONB,
    search_vector tsvector,
    PRIMARY KEY (business_id, attribute_key)
);


CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_TABLE_NAME = 'restaurant' THEN
        NEW.search_vector := to_tsvector('english', NEW.name || ' ' || NEW.address || ' ' || NEW.city || ' ' || NEW.state
                             || ' ' || NEW.postal_code || ' ' || NEW.latitude || ' ' || NEW.longitude || ' ' || NEW.stars ||
                             NEW.review_count || ' ' || NEW.is_open); --x
    ELSIF TG_TABLE_NAME = 'restaurant_categories' THEN
        NEW.search_vector := to_tsvector('english', NEW.category); --x
    ELSIF TG_TABLE_NAME = 'restaurant_parking' THEN
        NEW.search_vector := to_tsvector('english', NEW.parking_type); --x
    ELSIF TG_TABLE_NAME = 'restaurant_ambience' THEN
        NEW.search_vector := to_tsvector('english', NEW.vibe); --x
    ELSIF TG_TABLE_NAME = 'restaurant_music' THEN
        NEW.search_vector := to_tsvector('english', NEW.music); --x
    ELSIF TG_TABLE_NAME = 'restaurant_dietary' THEN
        NEW.search_vector := to_tsvector('english', NEW.dietary); --x
    ELSIF TG_TABLE_NAME = 'restaurant_dynamic_attributes' THEN --x
        NEW.search_vector := to_tsvector('english', NEW.attribute_key || ' '  || NEW.attribute_value);
    ELSIF TG_TABLE_NAME = 'restaurant_good_for_meal' THEN
        NEW.search_vector := to_tsvector('english', NEW.occasion); --x
    ELSIF TG_TABLE_NAME = 'restaurant_best_nights' THEN
        NEW.search_vector := to_tsvector('english', NEW.day_of_week); --x
    ELSIF TG_TABLE_NAME = 'restaurant_attributes' THEN
        NEW.search_vector := to_tsvector('english',
            COALESCE(NEW.restaurant_price_range, '') || ' ' ||
            COALESCE(NEW.wifi, '') || ' ' ||
            COALESCE(NEW.noise_level, '') || ' ' ||
            COALESCE(NEW.alcohol, '') || ' ' ||
            COALESCE(NEW.restaurants_attire, '') || ' ' ||
            COALESCE(NEW.ages_allowed, '') || ' ' ||
            COALESCE(CASE WHEN NEW.coat_check THEN 'Coat Check Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.take_out THEN 'Takeout Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.delivery THEN 'Delivery Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.caters THEN 'Catering Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.wheelchair THEN 'Wheelchair Accessible' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.happy_hour THEN 'Happy Hour' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.outdoor_seating THEN 'Outdoor Seating Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.tv THEN 'TV Available' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.reservation THEN 'Reservations Accepted' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.dogs_allowed THEN 'Dogs Allowed' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.smoking THEN 'Smoking Allowed' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.good_for_dancing THEN 'Good for Dancing' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.accepts_insurance THEN 'Accepts Insurance' ELSE '' END, '') || ' ' ||
            COALESCE(NEW.best_nights, '') || ' ' ||
            COALESCE(CASE WHEN NEW.byob THEN 'BYOB' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.corkage THEN 'Corkage Fee' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.byob_corkage THEN 'BYOB Corkage Fee' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.open_24_hours THEN 'Open 24 Hours' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.restaurant_counter_services THEN 'Counter Services Available' ELSE '' END, '')
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--trigger

CREATE INDEX idx_restaurant ON restaurant USING gin(search_vector);
CREATE INDEX idx_restaurant_categories ON restaurant_categories USING gin(search_vector);
CREATE INDEX idx_restaurant_parking ON restaurant_parking USING gin(search_vector);
CREATE INDEX idx_restaurant_ambience ON restaurant_ambience USING gin(search_vector);
CREATE INDEX idx_restaurant_best_nights ON restaurant_best_nights USING gin(search_vector);
CREATE INDEX idx_restaurant_dynamic_attributes ON restaurant_dynamic_attributes USING gin(search_vector);
CREATE INDEX idx_restaurant_hours ON restaurant_hours USING gin(search_vector);
CREATE INDEX idx_restaurant_music ON restaurant_music USING gin(search_vector);
CREATE INDEX idx_restaurant_good_for_meal ON restaurant_good_for_meal USING gin(search_vector);
CREATE INDEX idx_restaurant_dietary ON restaurant_dietary USING gin(search_vector);
CREATE INDEX idx_restaurant_attributes ON restaurant_attributes USING gin(search_vector);

CREATE TRIGGER trg_update_search_vector_restaurant
BEFORE INSERT OR UPDATE ON restaurant
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_categories
BEFORE INSERT OR UPDATE ON restaurant_categories
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_parking
BEFORE INSERT OR UPDATE ON restaurant_parking
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_ambience
BEFORE INSERT OR UPDATE ON restaurant_ambience
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_best_nights
BEFORE INSERT OR UPDATE ON restaurant_best_nights
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_dynamic_attributes
BEFORE INSERT OR UPDATE ON restaurant_dynamic_attributes
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_hours
BEFORE INSERT OR UPDATE ON restaurant_hours
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_music
BEFORE INSERT OR UPDATE ON restaurant_music
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_good_for_meal
BEFORE INSERT OR UPDATE ON restaurant_good_for_meal
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_dietary
BEFORE INSERT OR UPDATE ON restaurant_dietary
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

CREATE TRIGGER trg_update_search_vector_restaurant_attributes
BEFORE INSERT OR UPDATE ON restaurant_attributes
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();