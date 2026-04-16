import pandas as pd

from etl.extract import BaseExtractor
from etl.transform import BaseTransformer
from etl.load import Loader


class ETLPipeline():
    def __init__(self, extractor: BaseExtractor, transformer: BaseTransformer, loader: Loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, dry_run: bool=False) -> pd.DataFrame:
        # Extract
        data = self.extractor.extract()

        # Transform
        df = pd.json_normalize(data)
        self.transformer.transform(df)

        if dry_run:
            return df
        
         # TODO: Hvad sker der hvis transform returnerer en tom DataFrame? Bør load alligevel kaldes?

        # Load
        self.loader.load(df, append=True)

        return df
