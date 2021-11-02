from flask import Flask, jsonify, json, request
import requests
import json

app = Flask(__name__)


@app.route("/")
def nutrition():
    return "<p> Code Challenge for Juice Analytics </p> <a href=/get_total_hits> Return total hits"


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
