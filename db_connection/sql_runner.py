"""Module for running SQL queries against a database using SQLAlchemy."""
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

from sqlalchemy import Engine, Result, create_engine, text
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import database_exists, create_database


load_dotenv()
connection_string = os.getenv('DATABASE_URI')


class SQLRunner:
    """Run SQL queries against a given database engine."""

    def __init__(self, engine: Engine):
        """Initialize the SQLRunner with a SQLAlchemy engine.

        Args:
            engine (Engine): A SQLAlchemy Engine instance to connect to the database.
        """
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)

    def run_query(self, query: str | Path) -> Result[Any]:
        """Run a SQL query and return the results.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.

        Raises:
            FileNotFoundError: If the query is provided as a Path and the file does not exist.
        """
        if isinstance(query, Path):
            if not query.exists():
                raise FileNotFoundError(f"Query file '{query}' not found.")
            else:
                with open(query, 'r') as file:
                    query = file.read()

        with self.Session() as session:
            result = session.execute(text(query))
            return result

    
def get_engine() -> Engine:
    """Create a SQLAlchemy engine based on the configuration file.
    """
 #   connection_string = _get_connection_string(config_file)

    if not database_exists(connection_string):
        create_database(connection_string)

    return create_engine(connection_string)


'''
def _get_connection_string(config_file: Path) -> str:
    """Construct a database connection string from the configuration file.

    Args:
        config_file (Path): Path to the configuration file containing database connection details.
    """
    config = cp.ConfigParser()

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file '{config_file}' not found.")
    else:
        config.read(config_file)

    user = config['DBCONFIG']['User']
    password = config['DBCONFIG']['Password']
    host = config['DBCONFIG']['Host']
    port = config['DBCONFIG']['Port']
    database = config['DBCONFIG']['Database']

    return f'postgresql://{user}:{password}@{host}:{port}/{database}'
'''