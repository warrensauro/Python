def data_overview(df):
    row_count = len(df)
    column_count = len(df.columns)
    column_names = df.columns.tolist()
    data_types = df.dtypes.to_dict()


    meta = {
        "rows": row_count,
        "column count": column_count,
        "column names": column_names,
        "data types": data_types
    }
    return meta