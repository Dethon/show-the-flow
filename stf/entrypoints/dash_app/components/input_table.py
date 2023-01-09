from __future__ import annotations
import math
import pandas as pd
from dash import html, dcc, dash_table, Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
from stf.entrypoints.dash_app.components.base_component import BaseComponent
from stf.entrypoints.dash_app.components.unitable_input import UnitableInput
from stf.dependency_configurator import services

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


class InputTable(BaseComponent):
    class ids:
        data_table = lambda id: {"component": "InputTable", "subcomponent": "data_table", "aio_id": id}
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
        self.df = df

        datatable_props = self.add_defaults(datatable_props, DATA_TABLE_DEFAULTS)
        datatable_props["hidden_columns"] = datatable_props.get("hidden_columns", []) + [IDX_COL]
        datatable_props["data"] = []
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
                dcc.Store(data=services.dataset_service().add_to_cache(self.df.set_index(IDX_COL)), id=self.store_id),
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
            key: str,
        ) -> list[dict]:
            view = services.dataset_service().get_view(
                key=key, page=page, page_size=page_size, sort_by=sort_by, filter_query=filter_query
            )
            return view.reset_index(names=IDX_COL).to_dict("records")

        @callback(
            Output(self.store_id, "data"),
            Input(self.data_table_id, "derived_virtual_data"),
            Input(self.add_row_button_id, "n_clicks"),
            State(self.data_table_id, "page_current"),
            State(self.data_table_id, "page_size"),
            State(self.data_table_id, "sort_by"),
            State(self.data_table_id, "derived_filter_query_structure"),
            State(self.store_id, "data"),
        )
        def update_store(
            visible_data: list[dict],
            add_row_clicks: int,
            page: int,
            page_size: int,
            sort_by: list[dict[str, str]],
            filter_query: dict,
            key: str,
        ) -> str:
            key = services.dataset_service().add_to_cache_if_missing_key(key, self.df.set_index(IDX_COL))

            if add_row_clicks and ctx.triggered_id == self.add_row_button_id:
                return services.dataset_service().add_row_to_cached_dataset(key)
            elif visible_data is not None:
                input_df = pd.DataFrame.from_dict(visible_data)
                input_df = input_df.set_index(IDX_COL) if not input_df.empty else input_df
                return services.dataset_service().update_dataset_with_view(
                    updated_view_df=input_df,
                    key=key,
                    page=page,
                    page_size=page_size,
                    sort_by=sort_by,
                    filter_query=filter_query,
                )

            return key

        @callback(
            Output(self.data_table_id, "page_count"),
            Input(self.store_id, "data"),
            Input(self.data_table_id, "page_size"),
            Input(self.data_table_id, "derived_filter_query_structure"),
        )
        def update_page_count(key: str, n_rows: int, filter_query: dict) -> int | None:
            if not n_rows:
                raise PreventUpdate

            data_len = services.dataset_service().get_dataset_len_from_cache(key, filter_query=filter_query)
            if data_len == 0:
                return None

            return math.ceil(data_len / n_rows)

        @callback(Output(self.data_table_id, "page_size"), Input(self.page_size_input.input_id, "value"))
        def update_page_size(page_size: int) -> int:
            if not page_size:
                raise PreventUpdate
            return page_size

        self.table_view_interaction = table_view_interaction
        self.update_store = update_store
        self.update_page_size = update_page_size
        self.update_page_count = update_page_count

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
