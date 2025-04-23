import pandas as pd
import json
import numpy as np
import psycopg2
from jsonschema import validate, exceptions
from genson import SchemaBuilder
from code.backend.app.db.connection import connect

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

path_checkin = "../../../data/raw/yelp_dataset/yelp_academic_dataset_checkin.json"
path_business = "../../../data/raw/yelp_dataset/yelp_academic_dataset_business.json"
path_review = "../../../data/raw/yelp_dataset/yelp_academic_dataset_review.json"
path_tip = "../../../data/raw/yelp_dataset/yelp_academic_dataset_tip.json"
path_user = "../../../data/raw/yelp_dataset/yelp_academic_dataset_user.json"

checkins = []
business = []
review = []
tip = []
user = []
with open(path_business, "r") as json_file:
    for a in json_file:
        business.append(json.loads(a))
# with open(path_checkin, "r") as json_file:
#     for a in json_file:
#         checkins.append(json.loads(a))
# with open(path_review, "r") as json_file:
#     for a in json_file:
#         review.append(json.loads(a))
# with open(path_tip, "r") as json_file:
#     for a in json_file:
#         tip.append(json.loads(a))
# with open(path_user, "r") as json_file:
#     for a in json_file:
#         user.append(json.loads(a))
# print(min([len(a.keys()) for a in checkins]),
#       max([len(a.keys()) for a in checkins]))

builder = SchemaBuilder()
builder.add_object(business)
schema = builder.to_schema()
print(json.dumps(schema, indent=4))
with open("business_schema.txt", "w") as file:
    for a in json.dumps(schema, indent=4):
        file.write(a)
#print(sum(np.asarray(checkins).shape) == np.asarray(checkins).shape[0]) #check if 1d array (no more nested)

#print([type(a) for a in checkins[0]])
#{'business_id': string, 'date': string}

print(business[2040])
# print([type(a) for a in tip[0]])
# print([type(a) for a in business[0]])
# print([type(a) for a in user[0]])