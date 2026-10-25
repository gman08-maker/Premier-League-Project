import pandas as pd
from pathlib import Path 
def load_season(file_path, season):
    """
    Checks if file_path is a valid raw HTML file, it reads the HTML file into a pandas DataFrame and returns that.
    Additionally, it checks if the season is a valid string and adds a season column to the DataFrame. 
    Otherwise, it raises an appropriate error.

    Args:
        file_path (str or pathlib.Path): The path to the raw HTML file.
        season (str): The season to check and adds a season column to the DataFrame.
    Returns:
        pd.DataFrame: A DataFrame containing the data from the HTML file if both inputs are valid.
    """
    
    # Check if file_path is a valid raw HTML file
    if not isinstance(file_path, (str, Path)):
        raise TypeError("file_path must be a string or pathlib.Path object.")
    
    file_path = Path(file_path)
    
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path} is not a valid raw HTML file.")

    if file_path.suffix.lower() != '.html':
        raise ValueError(f"{file_path} is not a valid raw HTML file. It must have a .html extension.")
    
    # Check if season is a string
    if not isinstance(season, str):
        raise TypeError("season must be a string.")
    if season not in file_path.stem:
        raise ValueError("season must be a valid season string present in the file name.")
    
    # Read the HTML file into a pandas DataFrame
    tables = pd.read_html(file_path, encoding="utf-8")    
    if len(tables) != 1:
        raise ValueError(f"{file_path} must contain exactly one table. Found {len(tables)} tables.")
    season_df = pd.DataFrame(tables[0])
    season_df['Season'] = season
    
    
    return season_df