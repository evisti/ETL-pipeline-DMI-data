import pandas as pd
from sqlalchemy import Table
from db_connection import SQLRunner


class Loader():
    """
    Loader class responsible for loading transformed data into the target database table. It handles appending new records while ensuring unique IDs by retrieving the current maximum ID from the table.
    
    Args:
        runner (SQLRunner): An instance of SQLRunner to manage database connections and queries
        table (Table): The SQLAlchemy Table object representing the target database table for loading data

    Methods:
        load: Loads a DataFrame into the database table, appending new records with unique IDs
        _get_max_id_in_table: Retrieves the maximum ID currently present in the target database table
    """
    def __init__(self, runner: SQLRunner, table: Table):
        self.runner = runner
        self.table = table # TODO: ved ikke om den hører til her eller om et andet sted er bedre

    def load(self, df: pd.DataFrame, append: bool=True) -> None:
        """
        Loads a DataFrame into the target database table, appending new records with unique IDs if specified.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to be loaded into the database
            append (bool, optional): If True, new records will be appended to the existing table with unique IDs. If False, the table will be overwritten. Default is True.
        """
        if append:
            df.index = df.index + self._get_max_id_in_table() + 1
    
        with self.runner.engine.begin() as connection:
            df.to_sql(
                name=self.table.name, 
                con=connection, 
                if_exists='append', 
                index=True, 
                index_label='id')
    
    def _get_max_id_in_table(self) -> int:
        """
        Retrieves the maximum ID currently present in the target database table to ensure that new records are appended with unique IDs.

        Returns:
            int: The maximum ID in the table, or -1 if the table is empty (ensuring that indexing starts from 0 in empty tables).
        """
        query = (f'SELECT MAX(id) FROM {self.table.name};')
        result = self.runner.run_query(query)
        max_index = list(result)[0][0]

        # if table is empty, max_index will be None, so we return -1 to start indexing from 0
        return max_index if max_index else -1
