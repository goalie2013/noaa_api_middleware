import requests
from fastapi import status, HTTPException, Response
from schemas import *
from config import settings
from dotenv import load_dotenv
from typing import List
import time

load_dotenv()

def validate_get_request(dataset_id, dataset_type):
    match dataset_id:
        case DatasetParameter.SUMMARY:
            if (type(dataset_type) != SummaryParameter):
                print('Dataset PARAM TYPE SHOULD BE SUMMARY')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Improper path")
        case DatasetParameter.CLIMATE_NORMALS:
            if (type(dataset_type) != ClimateParameter):
                print('Dataset PARAM TYPE SHOULD BE CLIMATE')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Improper path")
        case DatasetParameter.PRECIP:
            if (type(dataset_type) != PptParameter):
                print('Dataset PARAM TYPE SHOULD BE Ppt')
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Improper path")
        case __:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Improper path")
    
    return 1;


def send_request_to_noaa(payload) -> List[dict]:
    """Send GET request to NOAA API and return the results, a list of objects """
    
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    # !! TODO !!
    headers = {'token': settings.api_token}

    start = time.perf_counter()
    response = requests.get(base_url, headers=headers, params=payload)
    finish = time.perf_counter()
    print(finish - start)
    print('response url', response.url)
    # print('response', response, response.json())
    data = response.json()
    print('metadata', data["metadata"])
    if data:
        return data["results"]
    
    return []
