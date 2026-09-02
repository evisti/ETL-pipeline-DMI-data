import pandas as pd
from abc import ABC, abstractmethod


class BaseTransformer(ABC):
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> None:
        pass

    def _date_formatting(self, df: pd.DataFrame, date_cols: str | list[str]) -> None:
        """
        Format specified columns as datetime.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be transformed
            date_cols (str | list[str]): Column name(s) to be formatted as datetime
        """
        df[date_cols] = df[date_cols].apply(pd.to_datetime)

    def _drop_duplicates(self, df: pd.DataFrame, subset_cols: str | list[str]=None) -> None:
        """
        Drop duplicate rows from the DataFrame based on specified columns.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be transformed
            subset_cols (str | list[str], optional): Column name(s) to consider for identifying duplicates. If None, all columns are considered. Defaults to None.
        """
        df.drop_duplicates(subset=subset_cols, inplace=True)

    def _coordinate_formatting(self, df: pd.DataFrame, coordinate_col: str) -> None:
        """
        Format a column containing coordinate pairs into separate longitude and latitude columns. 

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be transformed
            coordinate_col (str): The name of the column containing coordinate pairs (as lists or tuples of [longitude, latitude])
        """
        df['longitude'] = [coordinate[0] for coordinate in df[coordinate_col]]
        df['latitude'] = [coordinate[1] for coordinate in df[coordinate_col]]
        df.drop(columns=coordinate_col, inplace=True)
    
    def _reset_index(self, df: pd.DataFrame) -> None:
        df.reset_index(drop=True, inplace=True)


class StationTransformer(BaseTransformer):
    """
    Transformer class responsible for transforming station data extracted from the DMI API into a format suitable for loading into the database.
    It handles date formatting, coordinate extraction, column renaming, and dropping unnecessary columns. 

    Methods:
        transform: Transforms the input DataFrame in place, modifying it to match the desired schema
    """
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

        # format latitude and longitude
        self._coordinate_formatting(df, 'geometry.coordinates')

        # delete unnecessary columns
        df.drop(columns=['type', 'id', 'geometry.type', 'properties.updated'], inplace=True)

        # rename columns TODO: consider better renaming
        df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
        df.rename(columns={'parameterId': 'parameters'}, inplace=True)

        # TODO: Handle missing values


class ObservationTransformer(BaseTransformer):
    """
    Transformer class responsible for transforming observation data extracted from the DMI API into a format suitable for loading into the database.
    It handles date formatting, coordinate extraction, column renaming, and dropping unnecessary columns. 

    Methods:
        transform: Transforms the input DataFrame in place, modifying it to match the desired schema
    """
    def __init__(self):
        pass
    
    def transform(self, df: pd.DataFrame) -> None:
        self._reset_index(df)

        # change date columns dtype
        date_cols = ['properties.observed', 'extracted']
        self._date_formatting(df, date_cols)

        # format latitude and longitude
        self._coordinate_formatting(df, 'geometry.coordinates')

        # delete unnecessary columns
        df.drop(columns=['type', 'id', 'geometry.type', 'properties.created'], inplace=True)

        # rename columns TODO: consider better renaming
        df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
        df.rename(columns={'parameterId': 'parameter'}, inplace=True)

        # delete duplicate rows
        self._drop_duplicates(df)

        # TODO: Handle missing values
