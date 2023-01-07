import io
import base64
from typing import Iterable
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype


def concat_columns(dataframe: pd.DataFrame, *cols: str, sep: str = "", num_decimals: int = 2) -> np.ndarray:
    result = format_num_column(dataframe[cols[0]], num_decimals=num_decimals)
    for col in cols[1:]:
        result = result + sep + format_num_column(dataframe[col], num_decimals=num_decimals)

    return result.to_numpy()


def format_num_column(series: pd.Series, num_decimals: int = 2) -> pd.Series:
    if is_numeric_dtype(series):
        return series.astype(float).round(num_decimals).astype(str)
    return series.astype(str)


def df_from_csv_base64(base64_string: str) -> pd.DataFrame:
    _, content_string = base64_string.split(",")
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode("utf-8")))


def as_list(arg) -> Iterable:
    if not isinstance(arg, Iterable) or isinstance(arg, str):
        return [arg]
    else:
        return arg
