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
       
    if exists('data.json'):
        with open('data.json') as f:
            data = f.read()
            #print(data[len(data)-1])
            n = data[:len(data) - 1]
            
        with open('data.json', 'w') as f:
            #f.write(n)
            new_data = json.dumps(id_dict)
            new_data = new_data[1:]
            n = n + ',' + new_data
            f.write(n)

    else:
        with open('data.json', 'w') as f:
            json.dump(id_dict, f)


if __name__ =='__main__':
    save_list_as_obj(get_list_from_api(limit=900, offset=1))
    save_list_as_obj(get_list_from_api(limit=700, offset=901))
    
