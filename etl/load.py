import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime, ARRAY
from db_connection import SQLRunner


def stations_table(metadata: MetaData, name='stations') -> Table:
    table = Table(
        name, metadata,
        Column('id', Integer, primary_key=True),
        Column('owner', String(255)),
        Column('country', String(3)),
        Column('anemometerHeight', Float),
        Column('wmoCountryCode', String(4)),
        Column('operationFrom', DateTime),
        Column('parameters', ARRAY(String(50))),
        Column('created', DateTime),
        Column('barometerHeight', Float),
        Column('validFrom', DateTime),
        Column('type', String(50)),
        Column('stationHeight', Float),
        Column('regionId', Integer),
        Column('name', String(255)),
        Column('wmoStationId', String(5)),
        Column('operationTo', DateTime),
        Column('stationId', String(5)),
        Column('validTo', DateTime),
        Column('status', String(50)),
        Column('longitude', Float),
        Column('latitude', Float)
    )
    return table


def observations_table(metadata: MetaData, name='observations') -> Table:
    table = Table(
        name, metadata,
        Column('id', Integer, primary_key=True),
        Column('observed', DateTime),
        Column('extracted', DateTime),
        Column('parameter', String(50)),
        Column('value', Float),
        Column('stationId', String(5)),
        Column('latitude', Float),
        Column('longitude', Float)
    )
    return table


def spac_table(metadata: MetaData, name='spac') -> Table:
    table = Table(
        name, metadata,
        Column('id', Integer, primary_key=True),
        Column('timestamp', DateTime),
        Column('BME280.humidity', Float),
        Column('BME280.pressure', Float),
        Column('BME280.temperature', Float),
        Column('DS18B20.temperature', Float)
    )
    return table


def drop_tables(sql_runner: SQLRunner, metadata: MetaData) -> None:
    metadata.drop_all(sql_runner.engine)


def create_tables(sql_runner: SQLRunner, metadata: MetaData, dropfirst: bool=True) -> None:
    engine = sql_runner.engine

    if dropfirst: 
        drop_tables(engine, metadata)
    
    metadata.create_all(engine)

    print('\nTables created:', end=' ')
    print(*metadata.tables.keys(), sep=', ')


def get_max_id_in_table(sql_runner: SQLRunner, table: Table) -> None:
    query = (f'SELECT MAX(id) FROM {table.name};')
    result = sql_runner.run_query(query)
    max_index = list(result)[0][0]

    return max_index if max_index else -1


def load_to_sql(sql_runner: SQLRunner, table: Table, df: pd.DataFrame, append=True) -> None:
    if append:
        df.index = df.index + get_max_id_in_table(sql_runner, table) + 1
    
    with sql_runner.engine.begin() as connection:
        df.to_sql(
            name=table.name, 
            con=connection, 
            if_exists='append', 
            index=True, 
            index_label='id')

