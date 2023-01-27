import json
import requests
from os.path import exists
from config import settings
from dotenv import load_dotenv

load_dotenv()

def get_list_from_api(limit: int, offset: int):
    datatypes_url = f'https://www.ncei.noaa.gov/cdo-web/api/v2/datatypes?limit={limit}&offset={offset}'
    headers = {'token': settings.api_token}

    response_datatypes = requests.get(datatypes_url, headers=headers)
    data_datatypes = response_datatypes.json()
    
    return data_datatypes["results"]
    
def save_file(filename: str, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def save_list_as_obj(lst: list):
    """Convert API response from a list of objects to an object of objects; then save to a local json file. """
    
    id_map = _convert_to_dict(lst)
    _save_to_json(id_map)
    
def _convert_to_dict(lst: list):
    return {obj['id']: obj for obj in lst}

def _save_to_json(id_dict: dict):
    """Save dictionary to json file. If json file already exists,
       add to existing data. Splice existing and new data to combine
       into one JSON object. Setup this way bc will need to run 2x
       due to api data limit"""
       
    if exists('datatypes.json'):
        with open('datatypes.json') as f:
            data = f.read()
            #print(data[len(data)-1])
            n = data[:len(data) - 1]
            
        with open('datatypes.json', 'w') as f:
            #f.write(n)
            new_data = json.dumps(id_dict)
            new_data = new_data[1:]
            n = n + ',' + new_data
            f.write(n)

    else:
        save_file('datatypes.json', id_dict)


def get_first_n_dictionary_items(d: dict, n: int):
    d_items = d.items()
    first_n = list(d_items)[:n]
    return first_n

def get_last_n_dictionary_items(d: dict, n: int):
    d_items = d.items()
    first_n = list(d_items)[len(d_items) - n:]
    return first_n


if __name__ =='__main__':
    # save_list_as_obj(get_list_from_api(limit=900, offset=1))
    # save_list_as_obj(get_list_from_api(limit=700, offset=901))
    
    map1 = _convert_to_dict(get_list_from_api(limit=900, offset=1))
    print(get_last_n_dictionary_items(map1, 3))
    
    map2 = _convert_to_dict(get_list_from_api(limit=700, offset=901))
    print(get_first_n_dictionary_items(map2, 5))
    
    # Merge dictionaries together into map1
    map1.update(map2)
    
    save_file('data.json', map1)


