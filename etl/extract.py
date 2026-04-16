import requests
from abc import ABC, abstractmethod
from datetime import datetime


class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> list[dict]: #TODO: not sure about return type. Should I make it dataframe instead?
        pass

    def save(self) -> None: # TODO: would it be nice to save json file?
        pass

    def _make_request(self, url: str, params: dict, headers=None):
        '''
        Submit GET request with url and parameters, and convert result to DataFrame
        
        Args:
            url
            params
            headers
        '''
        timeout =  10 # seconds

        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        print('Fetching URL:', response.url)
        response.raise_for_status()

        return response.json()

    def _construct_datetime_str(self, from_time: datetime=None, to_time: datetime=None) -> str:
        '''
        Convert datetime to ISO format string

        Args:
            from_time
            to_time
        '''
        if from_time and to_time:
            return f'{from_time.isoformat()}Z/{to_time.isoformat()}Z'
    
        elif from_time and not to_time:
            return f'{from_time.isoformat()}Z'
    
        elif not from_time and to_time:
            return f'{to_time.isoformat()}Z'


class StationExtractor(BaseExtractor):
    def __init__(self, url, station_id: str=None):
        self.url = url
        self.station_id = station_id

    def extract(self) -> list[dict]:
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
    def __init__(self, url: str, station_id: str, parameter: str, from_time: datetime, to_time: datetime, limit: int=5000):
        self.url = url
        self.station_id = station_id
        self.parameter = parameter
        self.from_time = from_time
        self.to_time = to_time
        self.limit = limit

    def extract(self) -> list[dict]:
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


