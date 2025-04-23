# import pandas as pd
# import numpy as np
#
# import json
#
# dataset = []
# with open("../data/raw/yelp_dataset/yelp_academic_dataset_business.json", "r") as f:
#     data = []
#     for line in f:
#         data.append(json.loads(line))
#         #loads is for string like '{"name": "Alice", "age": 30, "city": "Wonderland"}'
#         #as opposed to
#         #load for being for {'name': 'Alice', 'age': 30, 'city': 'Wonderland'}
#     dataset.append(data)
# #{'business_id', 'name', 'address', 'city', 'state',
# # 'postal_code', 'latitude', 'longitude', 'stars', 'review_count', 'is_open',
# # 'attributes': {'BusinessAcceptsCreditCards', 'WheelchairAccessible',
# # 'RestaurantsTakeOut', 'BusinessParking': "{'garage', 'street', 'validated',
# # 'lot', 'valet'}", 'BikeParking', 'GoodForKids', 'Caters'},
# # 'categories', 'hours': {'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}}
# dataset = dataset[0]
# print(len(dataset))
# name = set([a["name"] for a in dataset if a["categories"] is not None and 'Food' in a["categories"]])
# food = [a for a in dataset if a["categories"] is not None and 'Food' in a["categories"]]
# print(food[1])
print("hello world")