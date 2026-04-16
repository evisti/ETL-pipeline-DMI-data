from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime, ARRAY

# TODO: look more into ORM

def station_table(metadata: MetaData, name='stations') -> Table:
    table = Table(
        name, metadata,
        Column('id', Integer, primary_key=True),
        Column('extracted', DateTime),
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


def observation_table(metadata: MetaData, name='observations') -> Table:
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
