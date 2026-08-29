import os
import pandas as pd

from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import MetaData

from db_connection import SQLRunner, get_engine

from etl.extract import StationExtractor, ObservationExtractor
from etl.transform import StationTransformer, ObservationTransformer
from etl.load import Loader
from etl.etl import ETLPipeline

from etl.tables import station_table, observation_table


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
to_time = from_time + timedelta(days=5)
station_id = '06072'
parameters = None # all parameters

# SQL connection
sql_runner = SQLRunner(get_engine(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE))

# SQL table metadata
metadata = MetaData()


def run_etl_observations():
    table = observation_table(metadata, name='observations')
#    sql_runner.create_tables(metadata)

    pipeline = ETLPipeline(
        extractor=ObservationExtractor(DMI_URL, station_id, parameters, from_time, to_time), 
        transformer=ObservationTransformer(), 
        loader=Loader(sql_runner, table)
    )
    df = pipeline.run(dry_run=True)
    print(df.head())


def run_etl_stations():

    table = station_table(metadata, name='station_test')
    #sql_runner.create_tables(metadata)

    pipeline = ETLPipeline(
        extractor=StationExtractor(DMI_URL), 
        transformer=StationTransformer(), 
        loader=Loader(sql_runner, table)
    )
    df = pipeline.run()
    print(df.head())
    print(df.info())


def main():
    pass


if __name__=='__main__':
    run_etl_observations()