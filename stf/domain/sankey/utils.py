import io
import base64
from itertools import cycle, islice
from typing import Iterable
import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from plotly.colors import hex_to_rgb


def concat_columns(dataframe: pd.DataFrame, *cols: str, sep: str = "", num_decimals: int = 2) -> np.ndarray:
    result = format_num_column(dataframe[cols[0]], num_decimals=num_decimals)
    for col in cols[1:]:
        result = result + sep + format_num_column(dataframe[col], num_decimals=num_decimals)

    return result.to_numpy()


def format_num_column(series: pd.Series, num_decimals: int = 2) -> pd.Series:
    if is_numeric_dtype(series):
        return series.astype(float).round(num_decimals).astype(str)
    return series.astype(str)


def get_rgba_colors(amount: int, scale: Iterable, opacity=1) -> np.ndarray:
    return np.array([f"rgba{hex_to_rgb(c) + (opacity,)}" for c in islice(cycle(scale), None, amount)])


def links_from_rows(rows: list[dict[str, str | float]]) -> pd.DataFrame:
    return pd.DataFrame.from_dict(rows)


def df_from_csv_base64(base64_string: str) -> pd.DataFrame:
    _, content_string = base64_string.split(",")
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
