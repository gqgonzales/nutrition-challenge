# Return average Calories per fluid oz for all products in JSON
# Meaning, print a json file with a tuple: AvgCalFlOz = ???

# ATTACK PLAN:
# Request the first 50 hits from the API
# Request the second 40 hits from API
# Merge the two dictionaries together OR extract the `hits` list out of each, then merge
# Filter by accessing the `hits` list in the response. Inside is a collection of dictionaries
# In these results dictionaries, there is another dictionary called `fields`
# For the results with "nf_serving_size_unit": "fl oz", calculate the average calories per fluid oz of each relevant product
# Then get the average calories per fl oz of that collective list.
# Return as a json string

import requests
import json

# ----------------------------------------- FIRST FIFTY -----------------------------------------


def avg_calories_per_fl_oz():

    # ----------------------------------------- FIRST FIFTY -----------------------------------------

    # Request data from API for first chunk of results with appropriate query strings
    first_fifty = requests.get(
        'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0:50&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_servings_per_container,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

    # print(first_fifty)

    json_response_one = first_fifty.json()

    # print(json_response_one["hits"])
    # This works for displaying first 50 as hits, but won't let us manipulate

    # hits_list_one = json.dumps(json_response_one["hits"])
    # THIS RETURNS A STRING

    hits_list_one = json_response_one["hits"]
    # THIS RETURNS A LIST

    # ----------------------------------------- LAST FORTY -----------------------------------------

    last_forty = requests.get(
        'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=50:100&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_servings_per_container,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

    # print(last_forty)

    json_response_two = last_forty.json()

    # print(json_response_two["hits"])
    # This works for displaying last 40 as JSON, but won't let us manipulate

    # hits_list_two = json.dumps(json_response_two["hits"])
    # THIS RETURNS A STRING

    hits_list_two = json_response_two["hits"]
    # THIS RETURNS A LIST

    # ----------------------------------------- JOINING LISTS -----------------------------------------

    joined_hit_list = hits_list_one + hits_list_two
    # Concatonating two strings. A string disguised as a list.
    # print(joined_hit_list)
    # jsonified = json.dumps(joined_hit_list)

    # A response looks like:
    # {"_index": "f762ef22-e660-434f-9071-a10ea6691c27", "_type": "item", "_id": "55e66556771ae2d64c6d5424", "_score": 1,
    #   "fields": {"item_name": "100% Juice, Orange Tangerine", "nf_calories": 130, "nf_serving_size_qty": 8, "nf_serving_size_unit": "fl oz"}
    # }

    # ----------------------------------------- FILTERING -------------------------------------------

    filtered = []

    liquids = 'fl oz'

    for product in joined_hit_list:
        if liquids in product['fields'].values():
            filtered.append(product)
        else:
            pass

    # return json.dumps(filtered)

    # ----------------------------------------- AVERAGING -------------------------------------------

    # dictionary values are stored as strings instead of integers, which means that to perform any kind of mathematical operation on them, you must convert them to an integer and back to a string.

    calories_list = []

    def calculate_calories(nf_calories, nf_servings_per_container, nf_serving_size_qty):
        return (
            ((int(nf_calories)) * (int(nf_servings_per_container))) /
            ((int(nf_serving_size_qty)) * (int(nf_servings_per_container)))
        )

    for product in filtered:
        attributes = product['fields'].items()
        # Returns tuples in a list. tuples are immutable.
        # int('nf_calories') * int('nf_servings_per_container')) / (int('nf_serving_size_qty') * int('nf_servings_per_container'))
        for attribute in attributes:
            if 'nf_calories' in attribute.keys():
                calories = attribute['nf_calories'].values()
            if 'nf_servings_per_container' in attribute.keys():
                servings_per_container = attribute['nf_servings_per_container'].values(
                )
            if 'nf_serving_size_qty' in attribute.keys():
                serving_size_qty = attribute['nf_serving_size_qty'].values()

            calories_per_oz = calculate_calories(
                calories, servings_per_container, serving_size_qty)

            # calories_per_oz = calculate_calories(
            #     int(attribute['nf_calories'].values()), int(attribute['nf_servings_per_container'].values()), int(attribute['nf_servings_per_container'].values()))

            calories_list.append(calories_per_oz)
        print(calories_list)

    # Formula for calories per oz in a given product:
    # cal_per_oz = (nf_calories * nf_servings_per_container) / (nf_serving_size_qty * nf_servings_per_container)

    return json.dumps(calories_list)
