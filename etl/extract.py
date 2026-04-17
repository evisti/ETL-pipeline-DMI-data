import requests
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseExtractor(ABC):
    '''
    Base class for data extractors. Defines common methods for making API requests.
    Subclasses must implement the extract method to retrieve data from specific sources.
    
    Methods:
        extract: Abstract method to be implemented by subclasses for data retrieval
        save: Optional method to save extracted data, can be overridden by subclasses
        _make_request: Helper method to perform GET requests and handle responses
        _construct_datetime_str: Helper method to format datetime parameters for API requests
    '''
    @abstractmethod
    def extract(self) -> list[dict[str, Any]]: #TODO: not sure about return type. Should I make it dataframe instead?
        pass

    def save(self) -> None: # TODO: would it be nice to save json file?
        pass

    def _make_request(self, url: str, params: dict[str, str | int], headers: dict[str, str] = None) -> dict[str, Any]:
        '''
        Submit GET request with url and parameters, and convert result to DataFrame

        Args:
            url (str): API endpoint URL
            params (dict): Dictionary of query parameters for the request
            headers (dict, optional): Optional dictionary of HTTP headers to include in the request
        
        Returns:
            dict: The JSON response from the API as a dictionary
        
        Raises:
            requests.exceptions.RequestException: If the request fails due to network issues, invalid responses, or other HTTP errors
        '''
        timeout =  10 # seconds

        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        print('Fetching URL:', response.url)
        response.raise_for_status()

        return response.json()

    def _construct_datetime_str(self, from_time: datetime | None = None, to_time: datetime | None = None) -> str | None:
        '''
        Convert datetime to ISO format string

        Args:
            from_time (datetime, optional): The starting datetime for the query range
            to_time (datetime, optional): The ending datetime for the query range
        '''
        if from_time and to_time:
            return f'{from_time.isoformat()}Z/{to_time.isoformat()}Z'
    
        elif from_time and not to_time:
            return f'{from_time.isoformat()}Z'
    
        elif not from_time and to_time:
            return f'{to_time.isoformat()}Z'


class StationExtractor(BaseExtractor):
    '''
    Extractor for retrieving station data from the DMI API. Inherits from BaseExtractor and implements the extract method to fetch station information based on optional station ID.
    
    Args:
        url (str): The base URL for the DMI API
        station_id (str, optional): ID of the station to retrieve data for. If None, data for all stations will be retrieved.
    
    Methods:
        extract: Fetches station data from the DMI API and returns it as a list of dictionaries, including an extraction timestamp
    '''
    def __init__(self, url: str, station_id: str | None = None):
        self.url = url
        self.station_id = station_id

    def extract(self) -> list[dict[str, Any]]:
        '''
        Fetches station data from the DMI API based on the specified station ID (if provided).
        
        Returns:
            list[dict[str, Any]]: A list of dictionaries containing station data, each with an 'extracted' timestamp indicating when the data was retrieved from the API.
        '''
        # define query parameters for the request
        query_params = {}
        if self.station_id: query_params['stationId'] = self.station_id

        # url for stations
        url = self.url + '/station/items'

        # retrive data
        response = self._make_request(url, query_params)
        features = response['features']

        # add timestamp to features
        features = [{**dic, 'extracted': response['timeStamp']} for dic in features]

        return features


class ObservationExtractor(BaseExtractor):
    '''
    Extractor for retrieving observation data from the DMI API. Inherits from BaseExtractor and implements the extract method to fetch observation data based on station ID, parameter, and time range.
    
    Args:
        url (str): The base URL for the DMI API
        station_id (str, optional): ID of the station to retrieve observations for. If None, data for all stations will be retrieved.
        parameter (str, optional): Specific parameter to filter observations by (e.g., temperature, wind speed). If None, all parameters will be retrieved.
        from_time (datetime): Starting datetime for the observation data retrieval range
        to_time (datetime): Ending datetime for the observation data retrieval range
        limit (int, optional): Maximum number of records to return per API request (default is 5000)
        
    Methods:
        extract: Fetches observation data from the DMI API and returns it as a list of dictionaries, including an extraction timestamp
    '''
    def __init__(self, url: str, station_id: str | None, parameter: str | None, from_time: datetime, to_time: datetime, limit: int=5000):
        self.url = url
        self.station_id = station_id
        self.parameter = parameter
        self.from_time = from_time
        self.to_time = to_time
        self.limit = limit

    def extract(self) -> list[dict[str, Any]]:
        '''
        Fetches observation data from the DMI API based on the specified parameters and time range.
        
        Returns:
            list[dict[str, Any]]: A list of dictionaries containing observation data, each with an 'extracted' timestamp indicating when the data was retrieved from the API.
        '''
        # define query parameters for the request

        datetime_str = self._construct_datetime_str(self.from_time, self.to_time)

        query_params = {
            'datetime' : datetime_str,
            'limit' : self.limit,  # maximum number of records to return
            'offset': 0}
        
        if self.parameter: query_params['parameterId'] = self.parameter
        if self.station_id: query_params['stationId'] = self.station_id

        # url for observations
        url = self.url + '/observation/items'

        # retrieve data
        data = []
        while True:
            response = self._make_request(url, query_params)
            features = response['features']

            # add timestamp to features
            features = [{**f, 'extracted': response['timeStamp']} for f in features]

            data += features

            number_returned = response['numberReturned']
            if number_returned < self.limit:
                break

            url = response['links'][-1]['href'] #TODO: offset kan maks være 500_000
            query_params = {}

        print('Records:', len(data))

        return data


class SpacExtractor(BaseExtractor):
    def __init__(self, url):
        self.url = url

    def extract(self):
        pass


