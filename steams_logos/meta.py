import os
import json


def load_from_json(item):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'data.json')
    with open(path) as json_data:
        data = json.load(json_data)
    return data.get(item, {})

# abbreviation replacements

REPLACES = load_from_json('replaces')

# exclude leagues without teams

EXCLUDES = load_from_json('excludes')
