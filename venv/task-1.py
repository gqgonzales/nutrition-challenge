# Return the total number of Juicy Juice products in JSON format.
# Meaning, print a json file with total_hits: 90

import requests
import json

# Request data from API with appropriate query strings
response = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&cal_min=0&cal_max=50000&fields=*&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')


print(response)

jsonResponse = response.json()

final = jsonResponse['total_hits']

dict_pairs = jsonResponse.items()
pairs_iterator = iter(dict_pairs)
total_hits = next(pairs_iterator)


with open('task-1-solution.json', 'w') as f:
    json.dump((total_hits), f)

# This solutuion generates a new file with that list json-ified.
