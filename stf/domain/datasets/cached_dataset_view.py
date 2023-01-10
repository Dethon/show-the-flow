from enum import Enum
from operator import attrgetter
import pandas as pd
from stf.domain.ports import DataframeCache

_OPERATORS = {
    ">=": "ge",
    "<=": "le",
    "<": "lt",
    ">": "gt",
    "!=": "ne",
    "=": "eq",
    "contains": "str.contains",
}


class DatasetOperation(Enum):
    DO_NOTHING = 0
    ROW_REMOVED = 1
    UPDATED_DATA = 2


class CachedDatasetView:
    def __init__(
        self,
        key: str,
        page: int,
        page_size: int,
        sort_by: list[dict[str, str]],
        filter_query: dict,
        cache: DataframeCache,
    ) -> None:
        self.key = key
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by
        self.filter_query = filter_query
        self.cache = cache
        self.df = cache.get_data(key)

    def get_view(self) -> pd.DataFrame:
        df = self.df
        if self.filter_query:
            df = self.filter_df(df, self.filter_query)
        if self.sort_by:
            df = self.sort_df(df, self.sort_by)
        return self.page_df(df, self.page, self.page_size)

    def update_dataset_with_view(self, updated_view_df: pd.DataFrame) -> str:
        oper = self._get_dataset_operation(updated_view_df)
        if oper == DatasetOperation.DO_NOTHING:
            return self.key
        if oper == DatasetOperation.UPDATED_DATA:
            self.df.update(updated_view_df)
            return self._update_in_cache(self.df)
        else:
            view_df = self.get_view()
            rows_to_remove = view_df.index[~view_df.index.isin(updated_view_df.index)]
            df = self.df[~self.df.index.isin(rows_to_remove)]
            return self._update_in_cache(df)

    def _get_dataset_operation(self, updated_view_df) -> DatasetOperation:
        view_df = self.get_view()
        if updated_view_df is None or self.df.empty or (updated_view_df.empty and len(self.df) == 1):
            return DatasetOperation.DO_NOTHING
        if len(updated_view_df) == len(view_df) - 1:
            return DatasetOperation.ROW_REMOVED
        if not updated_view_df.equals(view_df) and len(view_df) == len(updated_view_df):
            return DatasetOperation.UPDATED_DATA
        return DatasetOperation.DO_NOTHING

    def _update_in_cache(self, new_df: pd.DataFrame) -> str:
        self.df = new_df
        self.cache.remove_data(self.key)
        self.key = self.cache.add_data(new_df)
        return self.key

    @classmethod
    def filter_df(cls, df: pd.DataFrame, filter_query: dict) -> pd.DataFrame:
        operator = filter_query["value"]
        if operator == "&&":
            df = cls.filter_df(df, filter_query["left"])
            df = cls.filter_df(df, filter_query["right"])
        else:
            col_name = filter_query["left"]["value"]
            query = filter_query["right"]["value"]
            case_sensitive, operator = bool(operator[0] == "s"), operator[1:]  # noqa: F841
            df = df.loc[attrgetter(_OPERATORS[operator])(df[col_name])(query)]
        return df

    @classmethod
    def sort_df(self, df: pd.DataFrame, sort_by: list[dict[str, str]]) -> pd.DataFrame:
        cols = [col["column_id"] for col in sort_by]
        ascending = [col["direction"] == "asc" for col in sort_by]
        return df.sort_values(cols, ascending=ascending)

    @classmethod
    def page_df(cls, df: pd.DataFrame, page_current: int, page_size: int) -> pd.DataFrame:
        return df.iloc[page_current * page_size : (page_current + 1) * page_size]
