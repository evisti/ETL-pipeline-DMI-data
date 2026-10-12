import os
from datetime import datetime, timedelta
from sqlalchemy import MetaData

import etl
from db_connection import SQLRunner, get_engine

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Get DMI URL from environment variable
DMI_URL = os.getenv('DMI_URL')

# SQL connection
sql_runner = SQLRunner(get_engine())

# SQL table metadata
metadata = MetaData()

def run_etl_observations():
    # define table
    table = etl.observation_table(metadata, name='observations')
#    sql_runner.create_tables(metadata)

    # parameter definitions
    from_time = datetime(2025, 1, 1)
    to_time = from_time + timedelta(days=1)
    station_id = '06072'
    parameter = None # all parameters

    # create pipeline
    pipeline = etl.ETLPipeline(
        extractor=etl.ObservationExtractor(DMI_URL, from_time, to_time, station_id, parameter), 
        transformer=etl.ObservationTransformer(), 
        loader=etl.Loader(sql_runner, table)
    )

    # run pipeline
    df = pipeline.run(dry_run=True)

    print(df.head())


def run_etl_stations():
    # define table
    table = etl.station_table(metadata, name='station_test')
    #sql_runner.create_tables(metadata)

    # create pipeline
    pipeline = etl.ETLPipeline(
        extractor=etl.StationExtractor(DMI_URL), 
        transformer=etl.StationTransformer(), 
        loader=etl.Loader(sql_runner, table)
    )

    # run pipeline
    df = pipeline.run()

    print(df.head())
    print(df.info())


if __name__=='__main__':
    run_etl_observations()
