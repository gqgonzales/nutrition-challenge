# Return average Calories per fluid oz for all products in JSON
# Meaning, print a json file with a tuple: AvgCalFlOz = ???

# ATTACK PLAN:
# Request the first 50 hits from the API
# Request the second 40 hits from API
# Merge the two dictionaries together
# Filter by accessing the `hits` list in the response. Inside is a collection of dictionaries
# In these results dictionaries, there is another dictionary called `fields`
# For the results with "nf_serving_size_unit": "fl oz", calculate the average calories per fluid oz of each relevant product
# Then get the average calories per fl oz of that collective list.
# Return as json

import requests
import json


# ----------------------------------------- FIRST FIFTY -----------------------------------------

# Request data from API for first chunk of results with appropriate query strings
first_fifty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0:50&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_servings_per_container,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

# print(first_fifty)

json_response_one = first_fifty.json()

# hits_list_one = json.dumps(json_response_one["hits"])
# ^^ returns a string

hits_list_one = json_response_one["hits"]
# ^^ returns a list

# ----------------------------------------- LAST FORTY -----------------------------------------

last_forty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=50:100&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_servings_per_container,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

# print(last_forty)

json_response_two = last_forty.json()

# hits_list_two = json.dumps(json_response_two["hits"])
# ^^ returns a string

hits_list_two = json_response_two["hits"]
# ^^ returns a list

# ----------------------------------------- JOINING LISTS -----------------------------------------

joined_hit_list = hits_list_one + hits_list_two
# Concatenating two strings. A string disguised as a list.
# print(joined_hit_list)

# A response looks like:
# {"_index": "f762ef22-e660-434f-9071-a10ea6691c27", "_type": "item", "_id": "55e66556771ae2d64c6d5424", "_score": 1,
#   "fields": {"item_name": "100% Juice, Orange Tangerine", "nf_calories": 130, "nf_serving_size_qty": 8, "nf_serving_size_unit": "fl oz"}
# }

# ----------------------------------------- FILTERING -------------------------------------------

liquid_products = []
# !!! This list only accounts for products with "fl oz" as it's serving size unit.

liquids = 'fl oz'

for product in joined_hit_list:
    if liquids in product['fields'].values():
        liquid_products.append(product)
    else:
        pass

# return json.dumps(liquid_products)

# ----------------------------------------- AVERAGING -------------------------------------------

# Formula for calories per oz in a given product:
# cal_per_oz = (nf_calories * nf_servings_per_container) / (nf_serving_size_qty * nf_servings_per_container)


def calculate_calories(nf_calories, nf_servings_per_container, nf_serving_size_qty):
    return (
        ((int(nf_calories)) * (int(nf_servings_per_container))) /
        ((int(nf_serving_size_qty)) * (int(nf_servings_per_container)))
    )


calories_list = []

for product in liquid_products:
    calories_per_oz = calculate_calories(
        product['fields']['nf_calories'], product['fields']['nf_servings_per_container'], product['fields']['nf_serving_size_qty'])
    calories_list.append(calories_per_oz)
    # print(calories_list)

num_of_filtered_products = len(liquid_products)
total_calories = sum(calories_list)

average_calories_per_fl_oz = round(
    (total_calories / num_of_filtered_products), 2)

json_average = {"average_calories_per_fl_oz": average_calories_per_fl_oz}

with open('task-2-solution.json', 'w') as f:
    json.dump((json_average), f)
