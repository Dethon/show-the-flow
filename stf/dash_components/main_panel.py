import logging
import pandas as pd
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from plotly.graph_objects import Figure
from stf.sankey import Sankey, links_from_rows
from stf.dash_components.application import app
from stf.dash_components.components import (
    input_table,
    color_dropdown,
    unit_input,
    width_input,
    height_input,
    show_amout_check,
    sankey_graph,
)

default_layout = dict(margin=dict(autoexpand=False, b=25, l=25, t=25, r=25))


main_panel = html.Div(
    className="main-panel",
    children=[
        html.Div(
            className="chart-action-bar",
            children=[
                html.Div(
                    className="row",
                    children=[
                        color_dropdown,
                        width_input,
                        height_input,
                        unit_input,
                        show_amout_check,
                    ],
                )
            ],
        ),
        html.Div(className="chart-container", children=[sankey_graph]),
    ],
)


@app.callback(
    Output(sankey_graph, "figure"),
    Input(input_table, "data"),
    Input(width_input, "value"),
    Input(height_input, "value"),
    Input(show_amout_check, "value"),
    Input(unit_input, "value"),
    Input(color_dropdown, "value"),
)
def update_graph(
    rows: list[dict[str, str | float]], width: int, height: int, full_label: bool, unit: str, colorscale: str
) -> Figure:
    try:
        links_df = links_from_rows(rows)
        sankey = generate_graph(links_df, full_label, unit, colorscale, **default_layout, width=width, height=height)
        return sankey.get_figure()
    except Exception as exception:
        logging.exception(exception)
        raise PreventUpdate from exception


def generate_graph(links_df: pd.DataFrame, full_label: bool, unit: str, colorscale: str, **layout) -> Sankey:
    sankey = Sankey(links_df, colorscale=colorscale, unit=unit, full_label=full_label)
    sankey.update_layout(**layout)
    return sankey
