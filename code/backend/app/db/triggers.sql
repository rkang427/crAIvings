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

--for trigger
CREATE EXTENSION IF NOT EXISTS plpgsql;
--in case pre-existing


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
            COALESCE(NEW.hair_specializes_in, '') || ' ' ||
            COALESCE(CASE WHEN NEW.open_24_hours THEN 'Open 24 Hours' ELSE '' END, '') || ' ' ||
            COALESCE(CASE WHEN NEW.restaurant_counter_services THEN 'Counter Services Available' ELSE '' END, '')
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



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