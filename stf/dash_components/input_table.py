from __future__ import annotations
import math
from operator import attrgetter
import pandas as pd
import numpy as np
from dash import html, dcc, dash_table, Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
from stf.dash_components.base_component import BaseComponent
from stf.dash_components.unitable_input import UnitableInput


IDX_COL = "__index__"
DATA_TABLE_DEFAULTS = {
    "page_current": 0,
    "page_size": 10,
    "page_action": "custom",
    "filter_action": "custom",
    "filter_query": "",
    "sort_action": "custom",
    "sort_mode": "multi",
    "sort_by": [],
    "editable": True,
    "row_deletable": True,
}
_OPERATORS = {
    ">=": "ge",
    "<=": "le",
    "<": "lt",
    ">": "gt",
    "!=": "ne",
    "=": "eq",
    "contains": "str.contains",
}


class InputTable(BaseComponent):
    class ids:
        data_table = lambda id: {"component": "InputTable", "subcomponent": "data_table_id", "aio_id": id}
        store = lambda id: {"component": "InputTable", "subcomponent": "store", "aio_id": id}
        add_row_button = lambda id: {"component": "InputTable", "subcomponent": "add_row_button", "aio_id": id}
        page_size_input = lambda id: {"component": "InputTable", "subcomponent": "page_size_input", "aio_id": id}

    def __init__(
        self,
        df: pd.DataFrame | None = None,
        aio_id: str | None = None,
        className: str | None = None,
        **datatable_props,
    ) -> None:
        self.aio_id = aio_id or self.generate_uuid()
        self.data_table_id = self.ids.data_table(self.aio_id)
        self.store_id = self.ids.store(self.aio_id)
        self.add_row_button_id = self.ids.add_row_button(self.aio_id)
        self.page_size_input_id = self.ids.page_size_input(self.aio_id)

        df = df if df is not None else pd.DataFrame()
        df = df.reset_index(names=IDX_COL)
        columns, df = self._pre_process_df(df)

        datatable_props = self.add_defaults(datatable_props, DATA_TABLE_DEFAULTS)
        datatable_props["hidden_columns"] = datatable_props.get("hidden_columns", []) + [IDX_COL]
        datatable_props["data"] = df.to_dict("records")
        datatable_props["columns"] = columns

        self.page_size_input = UnitableInput(
            aio_id="page_size_input-" + self.aio_id,
            className="page-size-input",
            type="number",
            debounce=True,
            unit="Rows per page",
            value=datatable_props["page_size"],
            min=1,
        )
        super().__init__(
            [
                dcc.Store(data=df.to_dict("records"), id=self.store_id),
                dash_table.DataTable(id=self.data_table_id, **datatable_props),
                html.Button(id=self.add_row_button_id, children="+", className="add-row-button button"),
                self.page_size_input,
            ],
            className=self.class_name_concat(["input-table", className]),
        )

        @callback(
            Output(self.data_table_id, "data"),
            Input(self.data_table_id, "page_current"),
            Input(self.data_table_id, "page_size"),
            Input(self.data_table_id, "sort_by"),
            Input(self.data_table_id, "derived_filter_query_structure"),
            Input(self.store_id, "data"),
        )
        def table_view_interaction(
            page: int,
            page_size: int,
            sort_by: list[dict[str, str]],
            filter_query: dict,
            data: list[dict],
        ) -> list[dict]:
            df = pd.DataFrame.from_dict(data)
            df = InputTable.get_view_df(df, page, page_size, sort_by, filter_query)
            return df.to_dict("records")

        @callback(
            Output(self.store_id, "data"),
            Input(self.data_table_id, "data"),
            Input(self.add_row_button_id, "n_clicks"),
            State(self.data_table_id, "page_current"),
            State(self.data_table_id, "page_size"),
            State(self.data_table_id, "sort_by"),
            State(self.data_table_id, "derived_filter_query_structure"),
            State(self.store_id, "data"),
        )
        def update_store(
            data: list[dict],
            add_row_clicks: int,
            page: int,
            page_size: int,
            sort_by: list[dict[str, str]],
            filter_query: dict,
            stored_data: list[dict],
        ) -> list[dict]:
            if not data:
                raise PreventUpdate

            stored_df = pd.DataFrame.from_dict(stored_data).set_index(IDX_COL)
            if add_row_clicks and ctx.triggered_id == self.add_row_button_id:
                return InputTable.add_empty_row_df(stored_df).reset_index(names=IDX_COL).to_dict("records")

            input_df = pd.DataFrame.from_dict(data).set_index(IDX_COL)
            stored_paged_view = InputTable.get_view_df(stored_df, page, page_size, sort_by, filter_query)
            if input_df.equals(stored_paged_view):
                raise PreventUpdate

            stored_df.update(input_df)
            rows_to_remove = stored_paged_view.index[~stored_paged_view.index.isin(input_df.index)]
            stored_df = stored_df[~stored_df.index.isin(rows_to_remove)]
            return stored_df.reset_index(names=IDX_COL).to_dict("records")

        @callback(Output(self.data_table_id, "page_size"), Input(self.page_size_input.input_id, "value"))
        def update_page_size(page_size: int) -> int:
            if not page_size:
                raise PreventUpdate
            return page_size

        @callback(
            Output(self.data_table_id, "page_count"),
            Input(self.store_id, "data"),
            Input(self.data_table_id, "page_size"),
        )
        def update_page_count(data: list[dict], n_rows: int) -> int:
            if not n_rows:
                raise PreventUpdate
            return math.ceil(len(data) / n_rows)

        self.table_view_interaction = table_view_interaction
        self.update_store = update_store
        self.update_page_size = update_page_size
        self.update_page_count = update_page_count

    @classmethod
    def get_view_df(
        cls, df: pd.DataFrame, page: int, page_size: int, sort_by: list[dict[str, str]], filter_query: dict
    ) -> pd.DataFrame:
        if filter_query:
            df = InputTable.filter_df(df, filter_query)
        if sort_by:
            df = cls.sort_df(df, sort_by)
        return cls.page_df(df, page, page_size)

    @classmethod
    def add_empty_row_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        return pd.concat([df, pd.DataFrame([[np.nan] * df.shape[1]], columns=df.columns)], ignore_index=True)

    @classmethod
    def filter_df(cls, df: pd.DataFrame, filter_query: dict) -> pd.DataFrame:
        operator = filter_query["value"]
        if operator == "&&":
            df = cls.filter_df(df, filter_query["left"])
            df = cls.filter_df(df, filter_query["right"])
        else:
            col_name = filter_query["left"]["value"]
            query = filter_query["right"]["value"]
            case_sensitive, operator = bool(operator[0] == "s"), operator[1:]
            df = df.loc[attrgetter(_OPERATORS[operator])(df[col_name])(query)]
        return df

    @classmethod
    def sort_df(cls, df: pd.DataFrame, sort_by) -> pd.DataFrame:
        cols = [col["column_id"] for col in sort_by]
        ascending = [col["direction"] == "asc" for col in sort_by]
        return df.sort_values(cols, ascending=ascending)

    @classmethod
    def page_df(cls, df, page_current, page_size) -> pd.DataFrame:
        return df.iloc[page_current * page_size : (page_current + 1) * page_size]

    @classmethod
    def _pre_process_df(cls, df: pd.DataFrame) -> tuple[list[dict[str, str]], pd.DataFrame]:
        columns = [dict(name=c, id=c, type=cls._pd_type_to_dash_type(df[c])) for c in df.columns]
        return columns, df.astype({c["name"]: str for c in columns if c["type"] == "text"})

    @classmethod
    def _pd_type_to_dash_type(cls, series: pd.Series) -> str:
        if pd.api.types.is_numeric_dtype(series):
            return "numeric"
        elif pd.api.types.is_string_dtype(series):
            return "text"
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        else:
            return "text"
