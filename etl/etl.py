import pandas as pd

from sqlalchemy import Table

from etl.extractor import BaseExtractor
from etl.transformer import BaseTransformer
from etl.loader import Loader


class ETLPipeline():
    def __init__(self, extractor: BaseExtractor, transformer: BaseTransformer, loader: Loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, table: Table):
        # Extract
        data = self.extractor.extract()

        # Transform
        df = pd.json_normalize(data)
        self.transformer.transform(df)
        
        # Load
        self.loader.load(df, table)

    def dry_run(self) -> pd.DataFrame:
        # Extract
        data = self.extractor.extract()

        # Transform
        df = pd.json_normalize(data)
        self.transformer.transform(df)

        return df

