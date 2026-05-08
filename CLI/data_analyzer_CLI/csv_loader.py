import pandas as pd
import os
def load_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No file found at: {file_path}")
    try:  
        return pd.read_csv(file_path)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise ValueError(f"Corrupted data in {file_path}") from e