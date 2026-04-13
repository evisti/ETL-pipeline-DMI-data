import pandas as pd
from pathlib import Path
from datetime import datetime


# save to csv file
def save_to_csv(df: pd.DataFrame, save_folder: str, prefix: str, from_time: datetime, to_time: datetime):
    df.to_csv(Path(f'{save_folder}/{prefix}_{from_time.date().isoformat()}_{to_time.date().isoformat()}.csv'), index=False)


def read_file(filepath: Path) -> str:
    """
    Args:
        filepath (str): A Path to a file.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if isinstance(filepath, Path):
        if not filepath.exists():
            raise FileNotFoundError(f"File '{filepath}' not found.")
        else:
            with open(filepath, 'r') as file:
                result = file.read()

    return result


def write_file(content: str, filepath: Path):
    """
    Args:
        filepath (str): A Path to a file.
        content (str): The file content.

    Raises:
        FileNotFoundError: If the file path does not exist.
    """
    if isinstance(filepath, Path):
        if not filepath.parent.exists():
            raise FileNotFoundError(f"Path '{filepath.parent}' not found.")
        else:
            with open(filepath, 'w') as file:
                file.write(content)



def get_all_parameters(df_stations: pd.DataFrame) -> list[str]:
    return list(set([p for parameters in df_stations['parameters'] for p in parameters]))

