"""Module for running SQL queries against a database using SQLAlchemy."""
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, Result, MetaData, create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


class SQLRunner:
    """
    Run SQL queries against a given database engine and manage database tables.
    """

    def __init__(self, engine: Engine):
        """
        Initialize the SQLRunner with a SQLAlchemy engine for database connection.

        Args:
            engine (Engine): A SQLAlchemy Engine instance to connect to the database.
        """
        self.engine = engine
        self.Session = sessionmaker(self.engine)

    def run_query(self, query: str | Path) -> Result[Any]:
        """
        Run a SQL query and return the results.

        Args:
            query (str|Path): A SQL query as a string or a Path to a file containing the SQL query.

        Raises:
            FileNotFoundError: If the query is provided as a Path and the file does not exist.
        
        Returns:
            Result[Any]: The result of the executed SQL query.
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

    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table_name (str): The name of the table to check.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        return inspect(self.engine).has_table(table_name)

    def create_tables(self, metadata: MetaData, drop_first: bool=False) -> None:
        """
        Create all tables defined in the provided SQLAlchemy MetaData object in the database. Optionally drop existing tables first.
        
        Args:
            metadata (MetaData): A SQLAlchemy MetaData object containing table definitions to be created.
            drop_first (bool): If True, drop existing tables before creating new ones. Defaults to False.
        """
        if drop_first: 
            self.drop_tables(metadata)

        metadata.create_all(self.engine)

        print('\nTables created:', end=' ')
        print(*metadata.tables.keys(), sep=', ')

    def drop_tables(self, metadata: MetaData) -> None:
        """
        Drop all tables defined in the provided SQLAlchemy MetaData object from the database.

        Args:
            metadata (MetaData): A SQLAlchemy MetaData object containing table definitions to be dropped.
        """
        metadata.drop_all(self.engine)


def get_engine(user: str, password: str, host: str, port: str, database: str) -> Engine:
    """
    Create a SQLAlchemy engine for connecting to a PostgreSQL database. If the database does not exist, it will be created.

    Args:
        user (str): Database username
        password (str): Database password
        host (str): Database host address
        port (str): Database port
        database (str): Database name
    
    Returns:
        Engine: A SQLAlchemy Engine instance connected to the specified database.
    """
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

    if not database_exists(connection_string):
        create_database(connection_string)

    return create_engine(connection_string)
