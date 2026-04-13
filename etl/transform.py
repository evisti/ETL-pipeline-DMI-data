import pandas as pd


def date_formatting(df: pd.DataFrame, columns_with_date: list[str]): 
    # format date columns
    df[columns_with_date] = df[columns_with_date].apply(pd.to_datetime)


def drop_duplicates(df: pd.DataFrame, subset_name: str=None):
    if subset_name: 
        df.drop_duplicates(subset=[subset_name], inplace=True)
    else:
        df.drop_duplicates(inplace=True)


def geo_coordinates(df: pd.DataFrame, column_with_coordinates: str):
    # Split column_with_coordinates into two new columns (latitude and longitude), and delete the column_with_coordinates
    df['longitude'] = [coordinate[0] for coordinate in df[column_with_coordinates]]
    df['latitude'] = [coordinate[1] for coordinate in df[column_with_coordinates]]
    df.drop(columns=column_with_coordinates, inplace=True)


def reset_index(df: pd.DataFrame) -> pd.DataFrame:
    df.reset_index(drop=True, inplace=True)
    return df


def clean_stations(df: pd.DataFrame):

    print('Transform')

    # change date columns dtype to datetime
    columns_with_date = [
        'properties.operationFrom', 
        'properties.operationTo', 
        'properties.created', 
        'properties.validFrom', 
        'properties.validTo'
        ]
    date_formatting(df, columns_with_date)

    # latitude and longitude
    geo_coordinates(df, 'geometry.coordinates')

    # delete columns we don't want
    df.drop(columns=['type', 'id', 'geometry.type', 'properties.updated'], inplace=True)

    # rename columns
    df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
    df.rename(columns={'parameterId': 'parameters'}, inplace=True)

    # TODO: Replace missing values?

    print('Data info:')
    df.info()


def clean_observations(df: pd.DataFrame):

    print('Transform')
    
    # reset index
    reset_index(df)

    # change date columns dtype to datetime
    column_with_date = ['properties.observed', 'extracted']
    date_formatting(df, column_with_date)

    # latitude and longitude
    geo_coordinates(df, 'geometry.coordinates')

    # delete columns we don't want
    df.drop(columns=['type', 'id', 'geometry.type', 'properties.created'], inplace=True)

    # rename columns
    df.rename(lambda s: s.replace('properties.', ''), axis="columns", inplace=True)
    df.rename(columns={'parameterId': 'parameter'}, inplace=True)

    # delete dupllicate rows
    drop_duplicates(df)

    print('Data info:')
    df.info()


def clean_spac(df: pd.DataFrame):

    print('Transform')
    
    # change date columns dtype to datetime
    column_with_date = 'timestamp'
    date_formatting(df, column_with_date)

    # calculate temperature in celsius from raw reading
    df['DS18B20.temperature'] = df['reading.DS18B20.raw_reading'] / 1000 

    # delete columns we don't want
    df.drop(columns=['id', 'reading.DS18B20.device_name', 'reading.DS18B20.raw_reading'], inplace=True)

    # rename columns
    df.rename(lambda s: s.replace('reading.', ''), axis="columns", inplace=True)

    # delete dupllicate rows
    drop_duplicates(df)

    print('Data info:')
    df.info()
