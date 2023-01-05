import logging
from typing import Any

import pandas as pd
from dash import html, dcc, ctx, callback, no_update
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from plotly.graph_objects import Figure
from stf.domain import Sankey, df_from_csv_base64
from stf.dash_components import LabeledInput, UnitableInput, OptionalInput, InputTable
from stf.dash_pages.sankey_graph.constants import (
    TITLE,
    FILE_FORMAT_ERROR_MSG,
    DEFAULT_TABLE_PROPS,
    COLORSCALES,
    DEFAULT_LAYOUT,
)

color_input = LabeledInput(dcc.Dropdown, options=COLORSCALES, value="IceFire", clearable=False, label="Color palette")
default_figure = {"data": [{"type": "sankey"}]}
sankey_graph = dcc.Graph(className="chart", id="snk-graph", figure=default_figure)
width_input = LabeledInput(UnitableInput, type="number", unit="px", label="Width")
height_input = LabeledInput(UnitableInput, type="number", unit="px", label="Height")
font_size_input = LabeledInput(UnitableInput, type="number", placeholder="12", label="Font size", value=20)
npad_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node padding", unit="px", value=18)
nthick_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node thickness", unit="px", value=10)
nthick_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node thickness", unit="px", value=10)
show_amouts_input = LabeledInput(OptionalInput, placeholder="Unit", label="Show amounts")
input_table = InputTable(pd.read_csv("datasets/sample.csv"), **DEFAULT_TABLE_PROPS)
input_table_container = html.Div(input_table)
file_alert = dcc.ConfirmDialog(message="...", id="alert", displayed=False)
upload_box = dcc.Upload(
    className="upload-box", id="upload-data", children=html.Div(["Drag and Drop or ", html.A("Select Files")])
)


sidebar = html.Div(
    className="left-panel",
    children=[html.H1(TITLE), file_alert, upload_box, input_table_container],
)

main_panel = html.Div(
    className="main-panel",
    children=[
        html.Div(
            className="chart-action-bar",
            children=[
                html.Div(
                    className="row",
                    children=[
                        color_input,
                        width_input,
                        height_input,
                        npad_input,
                        nthick_input,
                        font_size_input,
                        show_amouts_input,
                    ],
                )
            ],
        ),
        html.Div(className="chart-container", children=[sankey_graph]),
    ],
)

layout = html.Div(className="container", children=[sidebar, main_panel])


@callback(
    Output(sankey_graph, "figure"),
    Input(input_table.store_id, "data"),
    Input(width_input.component.input_id, "value"),
    Input(height_input.component.input_id, "value"),
    Input(font_size_input.component.input_id, "value"),
    Input(npad_input.component.input_id, "value"),
    Input(nthick_input.component.input_id, "value"),
    Input(show_amouts_input.component.check_id, "value"),
    Input(show_amouts_input.component.input_id, "value"),
    Input(color_input.component, "value"),
    State(sankey_graph, "figure"),
)
def update_graph(
    rows: list[dict[str, str | float]],
    width: int,
    height: int,
    font_size: int,
    node_pad: int,
    node_thickness: int,
    full_label: bool,
    unit: str,
    colorscale: str,
    current_fig: dict[str, list[dict]],
) -> Figure:
    try:
        x_pos, y_pos = None, None
        trigger_id = ctx.triggered_id
        if trigger_id != input_table.data_table_id:
            x_pos, y_pos = get_position(current_fig)

        links_df = pd.DataFrame.from_dict(rows)
        sankey = Sankey(links_df, colorscale=colorscale, unit=unit, full_label=full_label, x_pos=x_pos, y_pos=y_pos)
        sankey.update_layout(**DEFAULT_LAYOUT, width=width, height=height, font_size=font_size)
        sankey.update_traces(node_pad=node_pad, node_thickness=node_thickness)
        return sankey.get_figure()
    except Exception as e:
        logging.exception(e)
        raise PreventUpdate from e


@callback(
    [Output(input_table_container, "children"), Output(file_alert, "displayed"), Output(file_alert, "message")],
    Input(upload_box, "contents"),
)
def update_table(file_contents: str) -> tuple[InputTable, bool, str]:
    if file_contents is None:
        raise PreventUpdate
    try:
        df = validate_df(df_from_csv_base64(file_contents))
        return InputTable(df, **DEFAULT_TABLE_PROPS), no_update, no_update
    except Exception as e:
        logging.exception(e)
        return no_update, True, FILE_FORMAT_ERROR_MSG


def validate_df(df: pd.DataFrame) -> pd.DataFrame:
    expected_headers = ["source", "amount", "target"]
    if set(expected_headers) != set(df.columns):
        raise TypeError
    return df


def get_position(figure: dict[str, list[dict]]) -> tuple[list | None, list | None]:
    node = figure["data"][0].get("node")
    x_state, y_state = (node.get("x"), node.get("y")) if node else (None, None)

    return x_state, y_state
