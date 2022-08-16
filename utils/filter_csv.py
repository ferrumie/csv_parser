from typing import IO
from dask import dataframe as dd
import pandas as pd

def parse_csv(csv_file: IO) -> IO:
    """collect chunk of csv files and filter the data."""
    dataset = dd.read_csv(csv_file, parse_dates=['Date'], blocksize=64000000)  # set 64 mb block size
    dataset['Number of Plays'] = dataset.groupby(['Song', 'Date'], sort=False, dropna=True)['Number of Plays'].transform('sum', meta=pd.Series(dtype='int', name='Number of Plays'))
    result_dataframe = dataset.drop_duplicates(['Song', 'Date'], ignore_index=False).rename(columns={'Number of Plays': 'Total Number of Plays for Date'})
    result_dataframe.to_csv("test/output_csv_*.csv", index=False)
    return