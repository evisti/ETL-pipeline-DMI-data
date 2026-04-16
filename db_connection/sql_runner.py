"""Module for running SQL queries against a database using SQLAlchemy."""
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, Result, MetaData, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class SQLRunner:
    """Run SQL queries against a given database engine."""

    def __init__(self, engine: Engine):
        """Initialize the SQLRunner with a SQLAlchemy engine.

        Args:
            engine (Engine): A SQLAlchemy Engine instance to connect to the database.
        """
        self.engine = engine
        self.Session = sessionmaker(self.engine)

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
        
    def table_exists(table_name: str) -> bool: # TODO
        pass

    def create_tables(self, metadata: MetaData, drop_first: bool=True) -> None:
        engine = self.runner.engine

        if drop_first: 
            self.drop_tables(metadata)

        metadata.create_all(engine)

        print('\nTables created:', end=' ')
        print(*metadata.tables.keys(), sep=', ')

    def drop_tables(self, metadata: MetaData) -> None:
        metadata.drop_all(self.runner.engine)


def get_engine(connection_string: str) -> Engine:
    """
    Create a SQLAlchemy engine
    """
    if not database_exists(connection_string):
        create_database(connection_string)

    return create_engine(connection_string)
