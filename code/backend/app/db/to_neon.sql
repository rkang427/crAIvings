
\c neondb;

\copy restaurant(id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_categories(business_id, category) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_categories.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_hours(business_id, day_of_week, open_time, close_time) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_hours.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_attributes(business_id, by_appointment_only, accept_credit_cards, restaurant_price_range, coat_check, take_out, delivery, caters, wifi, wheelchair, happy_hour, outdoor_seating, tv, reservation, dogs_allowed, alcohol, good_for_kids, restaurants_attire, restaurant_table_service, drive_thru, noise_level, accepts_bitcoin, smoking, good_for_dancing, accepts_insurance, best_nights, byob, corkage, byob_corkage, open_24_hours, restaurant_counter_services, ages_allowed) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_attributes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy restaurant_best_nights(business_id, day_of_week) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_best_nights.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_music(business_id, music) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_music.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy restaurant_dietary(business_id, dietary) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_dietary.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_parking(business_id, parking_type) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_parking.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_ambience(business_id, vibe)  FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_ambience.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
\copy restaurant_good_for_meal(business_id, occasion) FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_good_for_meal.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');

\copy restaurant_dynamic_attributes(business_id, attribute_key, attribute_value)  FROM '/Users/rheekang/docker_projects/crAIvings/code/data/clean/restaurant_dynamic_attributes.csv'  WITH (FORMAT csv, HEADER true, DELIMITER ',');
