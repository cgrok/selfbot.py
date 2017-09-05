import json

def load_json(path):
    with open(path) as f:
        return json.load(f)
