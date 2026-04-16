import pandas as pd
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> None:
        pass

    def _date_formatting(self, df: pd.DataFrame, date_cols: str | list[str]) -> None:
        df[date_cols] = df[date_cols].apply(pd.to_datetime)

    def _drop_duplicates(self, df: pd.DataFrame, subset_cols: str | list[str]=None) -> None:
        df.drop_duplicates(subset=subset_cols, inplace=True)

    def _coordinate_formatting(self, df: pd.DataFrame, coordinate_col: str) -> None:
        '''
        Split coordinate_col into two new columns, latitude and longitude, and delete the original column.
        '''
        df['longitude'] = [coordinate[0] for coordinate in df[coordinate_col]]
        df['latitude'] = [coordinate[1] for coordinate in df[coordinate_col]]
        df.drop(columns=coordinate_col, inplace=True)
    
    def _reset_index(self, df: pd.DataFrame) -> None:
        df.reset_index(drop=True, inplace=True)


class StationTransformer(BaseTransformer):
    def __init__(self):
        pass
    
    def transform(self, df: pd.DataFrame) -> None:
        # change date columns dtype
        date_cols = [
            'properties.operationFrom', 
            'properties.operationTo', 
            'properties.created', 
            'properties.validFrom', 
            'properties.validTo',
            'extracted'
        ]
        self._date_formatting(df, date_cols)

        # latitude and longitude
        self._coordinate_formatting(df, 'geometry.coordinates')

        # delete columns we don't want
        df.drop(columns=['type', 'id', 'geometry.type', 'properties.updated'], inplace=True)

        # rename columns
        df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
        df.rename(columns={'parameterId': 'parameters'}, inplace=True)                       # TODO: consider better renaming

        # TODO: Handle missing values


class ObservationTransformer(BaseTransformer):
    def __init__(self):
        pass
    
    def transform(self, df: pd.DataFrame) -> None:
        self._reset_index(df)

        # change date columns dtype
        date_cols = ['properties.observed', 'extracted']
        self._date_formatting(df, date_cols)

        # latitude and longitude
        self._coordinate_formatting(df, 'geometry.coordinates')

        # delete columns we don't want
        df.drop(columns=['type', 'id', 'geometry.type', 'properties.created'], inplace=True)

        # rename columns
        df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
        df.rename(columns={'parameterId': 'parameter'}, inplace=True)                       # TODO: consider better renaming

        # delete dupllicate rows
        self._drop_duplicates(df)

        # TODO: Handle missing values


class SpacTransformer(BaseTransformer):
    def __init__(self):
        pass
    
    def transform(self, df: pd.DataFrame) -> None:
        pass

