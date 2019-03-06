import json
import os

def load_json(path:str):
    # Load data from json file
    with open(path, "r") as file:  
        creds = json.load(file)

    return creds

def save_json(data, path:str, **kwargs):
    # dump data into json file
    if "makedirs" in kwargs.keys():
        dirrs = kwargs["makedirs"]
        for dirr in dirrs:
            os.makedirs(dirr, exist_ok=True)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)