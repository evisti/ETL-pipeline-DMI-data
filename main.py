import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import MetaData

import etl
from db_connection import SQLRunner, get_engine


# Load environment variables
load_dotenv()
DMI_URL = os.getenv('DMI_URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

# Parameter definitions
from_time = datetime(2025, 1, 1)
to_time = from_time + timedelta(days=1)
station_id = '06072'
parameters = None # all parameters

# SQL connection
sql_runner = SQLRunner(
    get_engine(
        user=USER, 
        password=PASSWORD, 
        host=HOST, 
        port=PORT, 
        database=DATABASE
    )
)

# SQL table metadata
metadata = MetaData()


def run_etl_observations():
    table = etl.observation_table(metadata, name='observations')
#    sql_runner.create_tables(metadata)

    pipeline = etl.ETLPipeline(
        extractor=etl.ObservationExtractor(DMI_URL, station_id, parameters, from_time, to_time), 
        transformer=etl.ObservationTransformer(), 
        loader=etl.Loader(sql_runner, table)
    )
    df = pipeline.run(dry_run=True)
    print(df.head())


def run_etl_stations():

    table = etl.station_table(metadata, name='station_test')
    #sql_runner.create_tables(metadata)

    pipeline = etl.ETLPipeline(
        extractor=etl.StationExtractor(DMI_URL), 
        transformer=etl.StationTransformer(), 
        loader=etl.Loader(sql_runner, table)
    )
    df = pipeline.run()
    print(df.head())
    print(df.info())


def main():
    pass


if __name__=='__main__':
    run_etl_observations()
    