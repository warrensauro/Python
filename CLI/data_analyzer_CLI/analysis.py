from pandas.api.types import is_numeric_dtype

def data_overview(df):
    row_count = len(df)
    column_count = len(df.columns)
    column_names = df.columns.tolist()
    data_types = df.dtypes.to_dict()


    meta = {
        "rows": row_count,
        "column_count": column_count,
        "column_names": column_names,
        "data_types": data_types
    }
    return meta

def filter_rows(df, column, value):
    if column not in df.columns:
        raise KeyError(f"No column named {column}")
    filtered_df = df[df[column] == value]
    return filtered_df

def sort_data(df, column, ascending=True):
    if column not in df.columns:
        raise KeyError(f"No column named {column}")
    sorted_df = df.sort_values(by=column, ascending=ascending)
    return sorted_df

def missing_values(df):
    missing_dict = df.isna().sum().to_dict()
    return missing_dict

def group_and_aggregate(df, group_column, agg_column, operation):
    op = operation.lower()
    missing = [col for col in [group_column, agg_column] if col not in df.columns]
    if missing:
        raise KeyError(f"Column/s not found: {','.join(missing)}")
    
    valid_op = ['mean', 'sum', 'count', 'min', 'max']
    if op not in valid_op:
        raise ValueError(f"Invalid operation. Choose from {valid_op}")
    
    is_int = is_numeric_dtype(df[agg_column])
    if op != 'count' and not is_int:
        raise ValueError(f"Cannot calculate {operation} on a text column: {agg_column}")
    result = df.groupby(group_column)[agg_column].agg(op)
    return result