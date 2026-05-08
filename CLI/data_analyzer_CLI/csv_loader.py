import pandas as pd

def load_csv(file_path):
    try:  
        dataframe = pd.read_csv(file_path)
        return dataframe
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found at: {file_path}")
    