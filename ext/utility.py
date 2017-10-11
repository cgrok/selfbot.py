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


def parse_equation(equation):
    eq = list(equation.replace('^', '**'))
    to_parse = ''
    for i, char in enumerate(eq):
        if char.isalpha():
            if eq[i-1].isdigit():
                if i != 0:
                    to_parse += f'{eq[i-1]}*{eq[i]}'
                else:
                    to_parse += char
            else:
                to_parse += char
        else:
            if i != len(eq)-1:
                if eq[i].isdigit():
                    if eq[i+1].isalpha():
                        continue
            to_parse += char
    return to_parse
