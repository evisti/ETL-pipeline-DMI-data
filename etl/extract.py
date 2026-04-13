import os
import requests
import pandas as pd

from datetime import datetime
from configparser import ConfigParser
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
DMI_URL = os.getenv('DMI_URL')
SPAC_URL = os.getenv('SPAC_URL')
TOKEN = os.getenv('SPAC_TOKEN')


def make_request(url: str, params: dict, headers: str=None):
    '''
    Submit GET request with url and parameters, and convert result to DataFrame
    '''
    timeout =  10 # seconds
    
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    print('Fetching URL:', response.url)
    response.raise_for_status()

    return response.json()
    

def construct_datetime_argument(from_time: datetime=None, to_time: datetime=None) -> str:
    '''
    Convert datetime to ISO format string
    '''
    if from_time and to_time:
        return f'{from_time.isoformat()}Z/{to_time.isoformat()}Z'
    
    elif from_time and not to_time:
        return f'{from_time.isoformat()}Z'
    
    elif not from_time and to_time:
        return f'{to_time.isoformat()}Z'
    
    else: 
        return None


def get_stations(station_id: str=None) -> pd.DataFrame:
    print('Extract')

    # define query parameters for the request
    query_params = {}
    if station_id: query_params['stationId'] = station_id

    # url for stations
    url = DMI_URL + '/station/items'

    # retrive data
    response = make_request(url, query_params)
    features = response['features']
    
    # add timestamp to features
    features = [{**dic, 'extracted': response['timeStamp']} for dic in features]
    
    records = pd.json_normalize(features)
    
    if records.empty:
        print('No data')

    return records


def get_observations(parameter: str, station_id: str, from_time: datetime, to_time: datetime, limit: int=5000) -> list[dict]:
    print('Extract')

    # define query parameters for the request
    query_params = {
        'datetime' : construct_datetime_argument(from_time=from_time, to_time=to_time),
        'limit' : limit,  # maximum number of records to return
        'offset': 0}
    if parameter: query_params['parameterId'] = parameter
    if station_id: query_params['stationId'] = station_id

    # url for observations
    url = DMI_URL + '/observation/items'

    # retrieve data
    data = []
    while True:
        response = make_request(url, query_params)
        features = response['features']

        # add timestamp to features
        features = [{**f, 'extracted': response['timeStamp']} for f in features]

        data += features

        number_returned = response['numberReturned']
        if number_returned < limit:
            break

        url = response['links'][-1]['href']
        query_params = {}

    print('Records:', len(data))

    return data


def get_spac(from_time: datetime=None, to_time: datetime=None, limit: int=5000):
    print('Extract')
    
    # get authorization token from configuration file
    config_file = Path(__file__).parents[1] / 'spac_config.ini'
    config = ConfigParser()

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    else:
        config.read(config_file)
    
    # define authorization token
    headers = {'Authorization': f'Bearer {TOKEN}'}

    # define query parameters for the request
    query_params = {}
    if limit: query_params['limit'] = limit # maximum number of records to return
    if from_time: query_params['from'] = construct_datetime_argument(from_time=from_time)

    # retrieve data
    response = make_request(SPAC_URL, query_params, headers)
    records = pd.json_normalize(response['records'])
    if records.empty:
        print('No data')

    return records
