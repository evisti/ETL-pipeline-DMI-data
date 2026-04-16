import os
import pandas as pd

from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import MetaData

from db_connection import SQLRunner, get_engine
from helper_functions import read_file, write_file

from etl.extract import StationExtractor, ObservationExtractor
from etl.transform import StationTransformer, ObservationTransformer
from etl.load import Loader
from etl.etl import ETLPipeline

from etl.tables import station_table, observation_table


# Load environment variables
load_dotenv()
DMI_URL = os.getenv('DMI_URL')
SPAC_URL = os.getenv('SPAC_URL')
TOKEN = os.getenv('SPAC_TOKEN')
DATABASE_URI = os.getenv('DATABASE_URI')

# Parameter definitions
from_time = datetime(2025, 1, 1)
to_time = from_time + timedelta(days=5)
station_id = '06072'
parameters = None # all parameters

sql_runner = SQLRunner(get_engine(DATABASE_URI))
metadata = MetaData()


'''
table = observation_table(metadata, name='observation_test')

pipeline = ETLPipeline(
    extractor=ObservationExtractor(DMI_URL, station_id, parameters, from_time, to_time), 
    transformer=ObservationTransformer(), 
    loader=Loader(sql_runner, table)
)
df = pipeline.dry_run()
print(df.head())
'''


table = station_table(metadata, name='station_test')
sql_runner.create_tables(metadata)

pipeline = ETLPipeline(
    extractor=StationExtractor(DMI_URL), 
    transformer=StationTransformer(), 
    loader=Loader(sql_runner, table)
)
df = pipeline.dry_run()
print(df.head())
print(df.info())
