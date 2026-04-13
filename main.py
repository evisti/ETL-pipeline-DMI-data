import pandas as pd
import json

from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import MetaData

from db_connection import SQLRunner, get_engine
from helper_functions import read_file, write_file
from etl.extract import get_stations, get_observations, get_spac
from etl.transform import clean_stations, clean_observations, clean_spac
from etl.load import stations_table, observations_table, spac_table, create_tables, load_to_sql



def extract_multiple():
    '''
    Extract all observations from 2025 and write to files
    '''
    start_time = datetime(2025, 1, 1)
    station_id = '06072'
    parameter = None # all parameters

    i = 1
    while True:
        end_time = start_time + timedelta(days=10)
        data = get_observations(parameter, station_id, start_time, end_time)

        # save as csv
        savefolder = 'data/2025_Aarhus_raw_json'
        filename = f'{i}_{station_id}_{start_time.date().isoformat()}_{end_time.date().isoformat()}.json'
        write_file(json.dumps(data), Path(f'{savefolder}/{filename}'))

        if end_time.year == 2026:
            break

        start_time = end_time
        i += 1


def transform_and_load():
    savefolder = Path('data/2025_Aarhus_raw_json')
    files = sorted(savefolder.glob('*.json'))

    # connect to database
    config_file = Path('./db_config.ini')
    sql_runner = SQLRunner(get_engine(config_file))

    # create metadata object
    metadata = MetaData()

    # define tables
    observations = observations_table(metadata, name='observations')

    # create tables in database
    create_tables(sql_runner, metadata, dropfirst=True)

    for f in files: 
        print(f)
        data = json.loads(read_file(f))
        df = pd.json_normalize(data)
        
        # transform
        clean_observations(df)

        # load
        load_to_sql(sql_runner, table=observations, df=df, append=True)


#extract_multiple()
#transform_and_load()








def etl_example():
    ######### EXTRACT #########

    # specify desired start and end time
    end_time = datetime.now()
    start_time = end_time - timedelta(days=1)

    # specify station and parameters for dmi observations
    station_id = '06072'
    parameter = 'wind_speed'

    # fetch data
    df_stations = get_stations()
    df_observations = get_observations(parameter, station_id, start_time, end_time)
    df_spac = get_spac()

    ######### TRANSFORM #########

    clean_stations(df_stations)
    clean_observations(df_observations)
    clean_spac(df_spac)

    ######### LOAD #########

    # connect to database
    config_file = Path('./db_config.ini')
    sql_runner = SQLRunner(get_engine(config_file))

    # create metadata object
    metadata = MetaData()

    # define tables
    stations = stations_table(metadata, name='stations_test')
    observations = observations_table(metadata, name='observations_test')
    spac = spac_table(metadata, name='spac_test')

    # create tables in database
    create_tables(sql_runner, metadata)

    # load data into database
    load_to_sql(sql_runner, table=stations, df=df_stations)
    load_to_sql(sql_runner, table=observations, df=df_observations)
    load_to_sql(sql_runner, table=spac, df=df_spac)


