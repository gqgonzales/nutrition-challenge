from flask import Flask, jsonify, json
import requests
import json

app = Flask(__name__)


@app.route("/")
def nutrition():
    return "<p> Code Challenge for Juice Analytics </p> <a href=/get_total_hits> Return total hits</a><br></br><a href=/avg_calories>Averge Calories per fl oz</a>"


@app.route("/loop")
def loop():
    try:
        # Initialize a employee list
        employeeList = []

        # create a instances for filling up employee list
        for i in range(0, 2):
            empDict = {
                'firstName': 'Roy',
                'lastName': 'Augustine'}
            employeeList.append(empDict)

            # convert to json data
            jsonStr = json.dumps(employeeList)

    except Exception:
        pass

    return jsonify(Employees=jsonStr)


@app.route("/get_total_hits")
def get_total_hits():
    response = requests.get(
        'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0%3A50&cal_min=0&cal_max=50000&fields=*&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

    jsonResponse = response.json()

    hits_response = jsonResponse['total_hits']
    # This returns just the value 90

    # dict_pairs = jsonResponse.items()
    # pairs_iterator = iter(dict_pairs)
    # total_hits = next(pairs_iterator)
    # This works for returning a list with a single key:value pair!

    jsonStr = json.dumps(hits_response)

    return jsonify(total_hits=jsonStr)
    # This returns an ugly verison

    # return "total_hits: " + jsonStr
    # Human readable version


@app.route("/avg_calories")
def avg_calories_per_fl_oz():

    # ----------------------------------------- FIRST FIFTY -----------------------------------------

    # Request data from API for first chunk of results with appropriate query strings
    first_fifty = requests.get(
        'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=0:50&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

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
        'https://api.nutritionix.com/v1_1/search/?brand_id=51db37d0176fe9790a899db2&results=50:100&cal_min=0&cal_max=50000&fields=item_name,nf_calories,nf_serving_size_qty,nf_serving_size_unit&appId=174401b5&appKey=a123b9aed02470ce919768e8ea96f9f7')

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
    # {"_index": "f762ef22-e660-434f-9071-a10ea6691c27", "_type": "item", "_id": "55592b2a61e715284d7ee8c2", "_score": 1,
    # "fields": {"item_name": "Freezer Pops, Tropical Punch", "nf_calories": 35, "nf_serving_size_qty": 1, "nf_serving_size_unit": "pop"}
    # }

    # ----------------------------------------- FILTERING -------------------------------------------

    filtered = []

    liquids = 'fl oz'

    for product in joined_hit_list:
        if liquids in product['fields'].values():
            filtered.append(product)
        else:
            pass

    return json.dumps(filtered)
    # ---------------------------

