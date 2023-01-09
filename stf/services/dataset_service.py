import io
import base64
import pandas as pd
import numpy as np
from stf.domain.ports import DataframeCache
from stf.domain.datasets import CachedDatasetView


class DatasetService:
    def __init__(self, cache: DataframeCache) -> None:
        self.cache = cache

    def get_cached_dataset_view(
        self, key: str, page: int, page_size: int, sort_by: list[dict[str, str]], filter_query: dict
    ) -> CachedDatasetView:
        return CachedDatasetView(key, page, page_size, sort_by, filter_query, self.cache)

    def df_from_csv_base64(self, base64_string: str) -> pd.DataFrame:
        _, content_string = base64_string.split(",")
        decoded = base64.b64decode(content_string)
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    def add_to_cache(self, df: pd.DataFrame) -> str:
        return self.cache.add_data(df)

    def add_to_cache_if_missing_key(self, key: str, df: pd.DataFrame) -> str:
        data = self.cache.get_data(key)
        if data is None:
            key = self.cache.add_data(df)
        return key

    def get_from_cache(self, key: str) -> pd.DataFrame:
        return self.cache.get_data(key)

    def is_in_cache(self, key: str) -> bool:
        return self.cache.get_data(key) is not None

    def get_dataset_len_from_cache(self, key: str, filter_query: dict | None = None) -> int:
        data = self.cache.get_data(key)
        if filter_query:
            data = CachedDatasetView.filter_df(data, filter_query)
        return len(data) if data is not None else 0

    def add_row_to_cached_dataset(self, key: str) -> str:
        df = self.cache.get_data(key)
        df = pd.concat([df, pd.DataFrame([[np.nan] * df.shape[1]], columns=df.columns)], ignore_index=True)
        self.cache.remove_data(key)
        return self.cache.add_data(df)

    def update_dataset_with_view(
        self,
        key: str,
        page: int,
        page_size: int,
        sort_by: list[dict[str, str]],
        filter_query: dict,
        updated_view_df: pd.DataFrame,
    ) -> str:
        dw = CachedDatasetView(key, page, page_size, sort_by, filter_query, self.cache)
        return dw.update_dataset_with_view(updated_view_df)

    def get_view(
        self,
        key: str,
        page: int,
        page_size: int,
        sort_by: list[dict[str, str]],
        filter_query: dict,
    ) -> pd.DataFrame:
        dw = CachedDatasetView(key, page, page_size, sort_by, filter_query, self.cache)
        return dw.get_view()
