import json

filepath = "config.json"
with open(filepath, "r") as jsonfile:
    config = json.load(jsonfile)
    print("Read successful")
