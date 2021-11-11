# Create an index of all Juicy Juice ingredients to the products that contain them
# (i.e., mango puree is in Tropical Mango Juice, Mango Blast, Banana Mango Punch).
# The data here is dirty; the final results don’t have to be perfect.

import requests
import json
import re

# ATTACK PLAN

# Combine the two lists again to get all 90 hits
# For each product, take the ingredients key:value pair out of the ['fields'] dictionary
# Split this key value pair into just a string with product['fields'].values(),
# then target the value product['fields']['nf_ingredient_statement'] ??? unsure about this
# Convert to uppercase characters with string.upper()
# Split the second half with string.split(", "), which will return a list of strings.


# Ingredient statements come back like this:
# "nf_ingredient_statement": "FILTERED WATER, APPLE JUICE FROM CONCENTRATE, PEAR JUICE FROM CONCENTRATE, ASCORBIC ACID (VITAMIN C), CITRIC ACID, NATURAL FLAVORS, PINEAPPLE JUICE FROM CONCENTRATE.",

# ----------------------------------------- FIRST FIFTY -----------------------------------------

# Request data from API for first chunk of results with appropriate query strings
first_fifty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0:50&cal_min=0&cal_max=50000&fields=item_name,nf_ingredient_statement&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

# print(first_fifty)

json_response_one = first_fifty.json()

# hits_list_one = json.dumps(json_response_one["hits"])
# ^^ returns a string

hits_list_one = json_response_one["hits"]
# ^^ returns a list

# ----------------------------------------- LAST FORTY -----------------------------------------

last_forty = requests.get(
    'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=50:100&cal_min=0&cal_max=50000&fields=item_name,nf_ingredient_statement&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

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

all_ingredients = set([])
# Sets do not allow duplicate values

for product in joined_hit_list:
    if product['fields']['nf_ingredient_statement'] != None:
        ingredients_list = product['fields']['nf_ingredient_statement'].upper().replace("(WATER", " ").replace(".", "").replace("  ", "").split(
            ", ")
        for ingreident in ingredients_list:
            all_ingredients.add(ingreident)

test_index = []

for ingredient in all_ingredients:
    prod_list = []
    ingredient_products_dict = {ingredient: prod_list}
    # if ingredient in product['fields'].values():
    if ingredient in product['fields']['nf_ingredient_statement'].upper():
        # {"ingredient": ["product_name_1", "product_name_2", "product_name_3"]}
        prod_list.append(product['fields']['item_name'])

        test_index.append(ingredient_products_dict)


# print(all_ingredients)
print("---------------------------------------------------------------------------------------")
print(test_index)
# Close!! This only loops for one product.
