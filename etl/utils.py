import pandas as pd
import requests
from difflib import get_close_matches
from pathlib import Path


def _read_file(filepath: Path) -> str:
    """
    Read the content of a file at the specified filepath.

    Parameters:
        filepath (Path): The path to a file.

    Returns:
        str: The content of the file.
    
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


def _write_file(content: str, filepath: Path):
    """
    Write content to a file at the specified filepath.

    Parameters:
        filepath (Path): The path to a file.
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


def extract_valid_parameters(url: str) -> tuple[list[str], list[str]]: 
    """
    Extract valid station IDs and observation parameters from a REST API endpoint.

    Parameters:
        url (str): The base URL of the REST API endpoint.
    
    Returns:
        list[str]: A sorted list of valid station IDs.
        list[str]: A sorted list of valid observation parameters.
    """
    # define url
    url += '/station/items'

    # request
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['features']
    df = pd.json_normalize(data)

    station_ids = list(df['properties.stationId'].unique())
    observation_params = list(set([p for params in df['properties.parameterId'] for p in params]))

    # save as txt files
    _write_file(
        '\n'.join(sorted(station_ids)), 
        filepath=Path(__file__).parent/'valid_station_ids.txt'
    )
    _write_file(
        '\n'.join(sorted(observation_params)), 
        filepath=Path(__file__).parent/'valid_observation_params.txt'
    )

    return station_ids, observation_params


def _get_valid_parameters(param_type: str) -> list[str]: 
    """
    Get valid parameters from a local file based on the specified parameter type.

    Parameters:
        param_type (str): The type of parameters to retrieve. Must be either 'stations' or 'observations'.
    
    Returns:
        list[str]: A list of valid parameters based on the specified param_type.
    """
    if param_type == 'stations':
        filename = 'valid_station_ids.txt'
    elif param_type == 'observations':
        filename = 'valid_observation_params.txt'
    else:
        raise ValueError(f"Invalid param_type '{param_type}'.\nMust be either 'stations' or 'observations'.")

    valid_params = _read_file(Path(__file__).parent/filename).split()

    return valid_params


def _check_param_validity(param_type: str, param: str):
    """
    Check the validity of a query parameter for the DMI API request. If the query parameter is not valid, raise a ValueError with suggestions for valid parameters.

    Parameters:
        param_type (str): The type of parameter to check. Must be either 'stations' or 'observations'.
        param (str): The query parameter to check for validity.
    """
    urls = dict(
        observations='https://www.dmi.dk/friedata/dokumentation/meteorological-observations-data',
        stations='https://www.dmi.dk/friedata/dokumentation/data/meteorological-observation-data-stations'
    )

    valid_params = _get_valid_parameters(param_type)

    if param not in valid_params:
        suggestions: list = get_close_matches(param, valid_params, n=5, cutoff=0.01)
        raise ValueError(f"Parameter with name '{param}' not found. Did you mean:\n{', '.join(suggestions)}?\n\nSee available parameters at {urls[param_type]}")
