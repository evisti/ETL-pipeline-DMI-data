import pandas as pd
from sqlalchemy import Table
from db_connection import SQLRunner


class Loader():
    def __init__(self, runner: SQLRunner, table: Table):
        self.runner = runner
        self.table = table # TODO: ved ikke om den hører til her eller om et andet sted er bedre

    def load(self, df: pd.DataFrame, append: bool=True) -> None:
        if append:
            df.index = df.index + self._get_max_id_in_table() + 1
    
        with self.runner.engine.begin() as connection:
            df.to_sql(
                name=self.table.name, 
                con=connection, 
                if_exists='append', 
                index=True, 
                index_label='id')
    
    def _get_max_id_in_table(self) -> None:
        query = (f'SELECT MAX(id) FROM {self.table.name};')
        result = self.runner.run_query(query)
        max_index = list(result)[0][0]

        return max_index if max_index else -1
