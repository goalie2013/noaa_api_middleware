from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from load_json import load_id_map, id_map_to_list, add_saved_data, add_lst
import api
from typing import List

app = FastAPI()

# Add CORS Middleware
origins = ["http://127.0.0.1:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Upload json object from 'data.json' local file
# id_map = load_id_map()
#id_lst = id_map_to_list(id_map)
# print('type idmap', type(id_map))


@app.get("/")
async def root():
    #return Response(status_code=status.HTTP_204_NO_CONTENT)
    return "NOAA"

    
@app.get("/{param1}/{param2}", response_model=List[ResModel])
async def bar(param1: DatasetParameter, param2: SummaryParameter | ClimateParameter | PptParameter, queries: Queries, map: dict = Depends(load_id_map)):
    """ Get Data from Dataset
    Find 'datasetid' for query: data_categories[param2]
    'datasetid', 'startdate', & 'enddate' are REQUIRED query parameters.
    Query parameters ('queries') for the NOAA API URL come from Request Body 
    and is the value of 'params' kwarg in the HTTP request """
        
    print('param1', param1)
    print('param2', param2, type(param2))
    print('data_categories[param2]', datasets[param2])
    print('queries dict', queries.dict())
    
    api.validate_get_request(param1, param2)
    
    dataset_id = datasets[param2]
    payload = queries.dict()
    payload.update({"datasetid": dataset_id})

    response_lst = api.send_request_to_noaa(payload)
    
    updated_lst = add_saved_data(response_lst, id_map=map)
    # add_lst(response_lst, id_lst)

    return updated_lst


@app.get("/{param1}")
async def baz(param1: EE, startdate: str, enddate: str, limit: int = 50, offset: int = 0, sortfield: str | None = None, sortorder: str | None = None, units: str | None = None, locationid: str | None = None):
    print('param1', param1)
    print('startdate', startdate)
    print('enddate', enddate) 