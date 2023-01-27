import json
import time

def load_id_map():
    """ Open data.json file, load, and return the data (dictionary) """
    
    print('running load_id_map...')
    with open('datatypes.json', 'r') as f:
        return json.load(f)
    
def id_map_to_list(id_map: dict):
    return [obj for id, obj in id_map.items()]
    
    
def add_saved_data(lst1: list, id_map: dict = load_id_map()):
    """ Add 'name' description into each dict in the first list from 
    the saved object [Use Dependency Injection to get the id_map (saved dict)]"""
    
    start = time.perf_counter()
    
    for obj in lst1:
        id: str = obj.get('datatype')
        saved_obj = id_map.get(id)
        #print('saved_obj', saved_obj)
        if saved_obj:
            #print('FOUND')
            obj['id'] = id
            obj['name'] = saved_obj.get('name')
            
    finish = time.perf_counter()
    print('total time', finish - start)
    
    return lst1
    

    
def add_lst(lst1, lst2):
    """ Add 'name' description into the first list from the saved list"""
    
    y = time.perf_counter()
    print('add_lst 1', time.perf_counter())
    for obj1 in lst1:
        id1 = obj1['datatype']
        for obj2 in lst2:
            if obj2['id'] == id1:
                obj1['id'] = id1
                obj1['name'] = obj2['name']
    print('add_lst 2', time.perf_counter())
    z = time.perf_counter()
    print(z - y)