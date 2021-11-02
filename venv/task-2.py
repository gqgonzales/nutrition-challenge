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


# Request data from API for first chunk of results with appropriate query strings
first_fifty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0:50&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

# print response
# print(first_fifty)
# <Response [200]>

json_response_one = first_fifty.json()

# print(json_response_one["hits"])
# This works for displaying first 50 as hits, but won't let us manipulate

hits_list_one = json.dumps(json_response_one["hits"])

# print(hits_list_one)

# ----------------------------------------- LAST FORTY -----------------------------------------

last_forty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=50:100&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

# print(last_forty)

json_response_two = last_forty.json()

# print(json_response_two["hits"])
# This works for displaying last 40 as JSON, but won't let us manipulate

hits_list_two = json.dumps(json_response_two["hits"])

# print(hits_list_two)

# ----------------------------------------- JOINING LISTS -----------------------------------------

joined_hit_list = hits_list_one + hits_list_two
# print(joined_hit_list)


# A response looks like:
# {"_index": "f762ef22-e660-434f-9071-a10ea6691c27", "_type": "item", "_id": "5678ba063893a666753a1248", "_score": 1, "fields": {"item_name": "Orange Tangerine Juice", "nf_calories": 70, "nf_serving_size_unit": "box"}},

# ----------------------------------------- ACESSING THE FIELDS IN DICTIONARIES -----------------------------------------

for entry in joined_hit_list:
    for fields in entry:
        print(entry[fields])


# ----------------------------------------- BREAK -----------------------------------------


# avg_calories_per_fluid_oz = (


# print(jsonResponse)

# with open('task-2-solution.json', 'w') as f:
#     json.dump(avg_calories_per_fluid_oz, f)


# avgList = []
# for key, value in joined_hit_list.items():
#     # value is all the data for key: product
#     avgList.append(sum(value) / float(len(value)))
