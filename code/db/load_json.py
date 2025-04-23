import pandas as pd
import json
#in terminal
#to install postgres 15
#brew install postgresql@15

#to start postgres
#brew services start postgresql

#switch to default superuser
# psql -d postgres
#to check all users
# \du

#to create a db
#CREATE DATABASE db_craivings;
#to create a user
# CREATE USER craivings_user WITH PASSWORD 'password';
# GRANT ALL PRIVILEGES ON DATABASE db_craivings TO craivings_user;
#\q

# quit and then connect to db
# psql -U craivings_user -d db_craivings


path_business = "/data/raw/yelp_academic_dataset_business.json"
path_checkin = "/data/raw/yelp_academic_dataset_checkin.json"
path_review = "/data/raw/yelp_academic_dataset_checkout.json"
path_tip = "/data/raw/yelp_academic_dataset_tip.json"
path_user = "/data/raw/yelp_academic_dataset_user.json"

