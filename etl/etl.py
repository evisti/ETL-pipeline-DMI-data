import pandas as pd

from etl.extract import BaseExtractor
from etl.transform import BaseTransformer
from etl.load import Loader


class ETLPipeline():
    """
    Class representing an ETL (extract, transform, load) pipeline. It orchestrates the extraction of data from a source, transformation of the data into a desired format, and loading of the transformed data into a target destination.

    Attributes:
        extractor (BaseExtractor): An instance of a class that implements the BaseExtractor class, responsible for extracting data from a source.
        transformer (BaseTransformer): An instance of a class that implements the BaseTransformer class, responsible for transforming the extracted data into a desired format.
        loader (Loader): An instance the Loader class, responsible for loading the transformed data into a target destination (e.g., a database).

    Methods:
        run: Executes the ETL process by extracting data, transforming it, and optionally loading it into the target destination if dry_run is set to False. Returns the transformed DataFrame.
    """
    def __init__(self, extractor: BaseExtractor, transformer: BaseTransformer, loader: Loader):
        """
        Initializes an instance of the ETLPipeline class with the specified extractor, transformer, and loader.

        Parameters:
            extractor (BaseExtractor): An instance of a class that implements the BaseExtractor class, responsible for extracting data from a source.
            transformer (BaseTransformer): An instance of a class that implements the BaseTransformer class, responsible for transforming the extracted data into a desired format.
            loader (Loader): An instance the Loader class, responsible for loading the transformed data into a target destination (e.g., a database).
        """
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, dry_run: bool=False) -> pd.DataFrame:
        """
        Executes the ETL process by extracting data, transforming it, and optionally loading it into the target destination if dry_run is set to False.

        Parameters:
            dry_run (bool, optional): If True, the ETL process will be executed without loading the transformed data into the target destination. Default is False.
        
        Returns:
            pd.DataFrame: The transformed DataFrame.
        """
        # extract
        data = self.extractor.extract()

        df: pd.DataFrame = pd.json_normalize(data)

        if df.empty:
            print('No data was extracted')
            return df

        # transform
        self.transformer.transform(df)
            
        # load
        if not dry_run:
            self.loader.load(df, append=True)

        return df
