import json

with open('data/poets.json', 'r', encoding="utf-8") as f:
    poets = json.load(f)['poets']

with open('data/bohour.json', 'r', encoding='utf-8') as f:
    bohours = json.load(f)['data']

with open('data/qawafi.json', 'r', encoding='utf-8') as f:
    qafiyah = json.load(f)['data']

def merge_dicts_by_name(dict_list):
    merged_dict = {}
    for item in dict_list:
        name = item.get('name')
        if name:
            merged_dict[name] = item
    return merged_dict

poets = merge_dicts_by_name(poets)
bohours = merge_dicts_by_name(bohours)

def load_poets():
    '''
    returns a dictionary of poets, structured as follows:

    Key: "name"
    Value: A dictionary containing the following keys:
    
    - "name": The poet's name in Arabic.
    - "name_en": The poet's name in English.
    - "description": Instructions for generating prompts.
    - "poems": A nested dictionary where each key represents a bahr (in English)

        {
            '<bahr1>': [
                ['<poem1-line1>', '<poem1-line2>', ...],
                ...
            ],
            ...
        }

    Example output:
    {
        "name": "نزار قباني",
        "name_en": "Nizar Qabbani",
        "description": "أنت نزار قباني، ...",
        "poems": {
            "baseet": [
                ['في الحب', 'في الفراق', ...],
                ...
            ]
        }
    }
    '''
    return poets

def load_bohours():
    '''
    Returns a dictionary of bohours, structured as follows:

    Key: "name"
    Value: A dictionary containing:
    
    - "name": Bahr's name in Arabic (string).
    - "name_en": Bahr's name in English (string).
    - "wazn": Bahr's wazn in Arabic (string, e.g., "mustaf3loun mustaf3loun mustaf3loun").
    - "pattern": Bahr's pattern represented in 0s and 1s (string).

    Example output:
    {
        "name": "الطويل",
        "name_en": "Musta'filun",
        "wazn": "فعولن مفاعيلن فعولن مفاعيلن",
        "pattern": "110111010101101110110"
    }
    '''
    return bohours

def load_qafiyas():
    '''
    Returns a list of words
    '''
    return qafiyah
