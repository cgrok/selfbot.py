import json

def load_json(path):
	try:
	    with open(path) as f:
	        return json.load(f)
	except:
		return {}

def save_json(data, path, **kwargs):
    with open(path, 'w') as f:
        json_data = json.dumps(data, indent=4, **kwargs)
        return f.write(json_data)