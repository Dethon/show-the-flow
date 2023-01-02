import logging
import pandas as pd
from dash import html, ctx, callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from plotly.graph_objects import Figure
from stf.domain import Sankey, links_from_rows
from stf.dash_components.components import (
    input_table,
    color_dropdown,
    unit_input,
    width_input,
    height_input,
    font_size_input,
    node_pad_input,
    node_thickness_input,
    show_amout_check,
    sankey_graph,
    add_label,
)

default_layout = dict(margin=dict(autoexpand=True, b=25, l=25, t=25, r=25))


main_panel = html.Div(
    className="main-panel",
    children=[
        html.Div(
            className="chart-action-bar",
            children=[
                html.Div(
                    className="row",
                    children=[
                        add_label(color_dropdown, "Color palette", "input-label"),
                        add_label(width_input, "Width", "input-label"),
                        add_label(height_input, "Height", "input-label"),
                        add_label(unit_input, "Unit", "input-label"),
                        add_label(font_size_input, "Font size", "input-label"),
                        add_label(node_pad_input, "Node padding", "input-label"),
                        add_label(node_thickness_input, "Node thickness", "input-label"),
                        show_amout_check,
                    ],
                )
            ],
        ),
        html.Div(className="chart-container", children=[sankey_graph]),
    ],
)


@callback(
    Output(sankey_graph, "figure"),
    Input(input_table, "data"),
    Input(width_input, "value"),
    Input(height_input, "value"),
    Input(font_size_input, "value"),
    Input(node_pad_input, "value"),
    Input(node_thickness_input, "value"),
    Input(show_amout_check, "value"),
    Input(unit_input, "value"),
    Input(color_dropdown, "value"),
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
        if trigger_id != input_table.id:
            x_pos, y_pos = get_position(current_fig)

        links_df = links_from_rows(rows)
        sankey = Sankey(links_df, colorscale=colorscale, unit=unit, full_label=full_label, x_pos=x_pos, y_pos=y_pos)
        sankey.update_layout(**default_layout, width=width, height=height, font_size=font_size)
        sankey.update_traces(node_pad=node_pad, node_thickness=node_thickness)
        return sankey.get_figure()
    except Exception as e:
        logging.exception(e)
        raise PreventUpdate from e


def get_position(figure: dict[str, list[dict]]) -> tuple[list | None, list | None]:
    node = figure["data"][0].get("node")
    x_state, y_state = (node.get("x"), node.get("y")) if node else (None, None)

    return x_state, y_state
