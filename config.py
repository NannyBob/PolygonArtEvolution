import json

with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    print("Read successful")
