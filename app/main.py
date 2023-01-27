from fastapi import FastAPI, Depends, Request, status, HTTPException
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
    return {"message":"NOAA"}

    
@app.get("/{param1}/{param2}")
async def bar(param1: DatasetParameter, param2: SummaryParameter | ClimateParameter | PptParameter, request: Request, queries: Queries | None = None, map: dict = Depends(load_id_map)):
    """ Get Data from Dataset
    Find 'datasetid' for query: data_categories[param2]
    'datasetid', 'startdate', & 'enddate' are REQUIRED query parameters.
    Query parameters ('queries') for the NOAA API URL come from Request Body 
    and is the value of 'params' kwarg in the HTTP request """
        
    api.validate_get_request(param1, param2)

    query_dict = parse_queries(request)

    print('data_categories[param2]', datasets[param2])
    #print('queries dict', queries.dict())
    
    # Get payload from request body (Queries) and add Dataset ID to payload
    dataset_id = datasets[param2]

    """ Request body has priority over query params
    # If request body is None --> If query_parser is None --> ERROR
    # If request body is None --> Set payload to query_parser dictionary
    # Else, request body has data --> Set payload from body
    # Add datasetID to payload 
    """
    if queries is None:
        print('queries IS NONE')
        if query_dict is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="startdate and endate required as body or query parameters")
        if query_dict.get('startdate') is None or query_dict.get('enddate') is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="startdate and endate required as body or query parameters")
        payload = query_dict
    else:
        payload = queries.dict()
    
    payload.update({"datasetid": dataset_id}) 
    
    print('payload', payload)


    # Send GET Request to NOAA API
    response_lst = api.send_request_to_noaa(payload)

    # Add saved json data to response_lst    
    updated_lst = add_saved_data(response_lst, id_map=map)
    # updated_lst = add_lst(response_lst, id_lst)

    return updated_lst
    return 's'



#@app.get("/{param1}/{param2}", response_model=List[ResModel])
#async def bazz(param1: DatasetParameter, param2: SummaryParameter | ClimateParameter | PptParameter, startdate: str, enddate: str, limit: int = 50, offset: int = 0, datatypeid: str | None = None, sortfield: str | None = None, sortorder: str | None = None, units: str | None = None, locationid: str | None = None):
#    print('param1', param1)
#    print('startdate', startdate)
#    print('enddate', enddate) 


@app.get("/{param1}")
async def baz(param1: EE, startdate: str, enddate: str, limit: int = 50, offset: int = 0, datatypeid: str | None = None, sortfield: str | None = None, sortorder: str | None = None, units: str | None = None, locationid: str | None = None):
    print('param1', param1)
    print('startdate', startdate)
    print('enddate', enddate) 
    print('locationid', locationid)
    
    
    
def parse_queries(request: Request):
    print(str(request.query_params), type(request.query_params))
    params = str(request.query_params)
    if not params:
        print('NO QUERY PARAMETERS')
        return None
    
    # String --> List
    params_lst = params.split('&')
    print('params_lst', params_lst)
    
    # Change string to key:value pair, split at '='
    # then add it to a dict
    new_dict = {}
    for el in params_lst:
        x = el.split('=')
        new_dict.update({x[0]: x[1]})
        
    #if not new_dict:
    #    return None
    
    q = Q(**new_dict)
    print('q.__dict__',q.__dict__)
    
    new_dict.update({'limit': 50, 'offset': 0})
    print('new_dict', new_dict)
    
    return new_dict