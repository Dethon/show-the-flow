import logging
from dash import html, dcc, ctx, callback
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from plotly.graph_objects import Figure
from stf.domain import Sankey, links_from_rows
from stf.dash_components import LabeledInput, UnitableInput, OptionalInput
from stf.dash_components.components import input_table

DEFAULT_LAYOUT = dict(margin=dict(autoexpand=True, b=25, l=25, t=25, r=25))
COLORSCALES = ["IceFire", "Twilight", "HSV", "mrybm", "mygbm", "Edge"]

color_dropdown = LabeledInput(
    dcc.Dropdown, className="dropdown", options=COLORSCALES, value="IceFire", clearable=False, label="Color palette"
)
default_figure = {"data": [{"type": "sankey"}]}
sankey_graph = dcc.Graph(className="chart", id="snk-graph", figure=default_figure)
width_input = LabeledInput(UnitableInput, type="number", unit="px", label="Width")
height_input = LabeledInput(UnitableInput, type="number", unit="px", label="Height")
font_size_input = LabeledInput(UnitableInput, type="number", placeholder="12", label="Font size", value=20)
npad_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node padding", unit="px", value=18)
nthick_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node thickness", unit="px", value=10)
nthick_input = LabeledInput(UnitableInput, type="number", placeholder="20", label="Node thickness", unit="px", value=10)
show_amouts_input = LabeledInput(OptionalInput, placeholder="Unit", label="Show amounts")

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


@callback(
    Output(sankey_graph, "figure"),
    Input(input_table, "data"),
    Input(width_input.component.input_id, "value"),
    Input(height_input.component.input_id, "value"),
    Input(font_size_input.component.input_id, "value"),
    Input(npad_input.component.input_id, "value"),
    Input(nthick_input.component.input_id, "value"),
    Input(show_amouts_input.component.check_id, "value"),
    Input(show_amouts_input.component.input_id, "value"),
    Input(color_dropdown.component, "value"),
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
        sankey.update_layout(**DEFAULT_LAYOUT, width=width, height=height, font_size=font_size)
        sankey.update_traces(node_pad=node_pad, node_thickness=node_thickness)
        return sankey.get_figure()
    except Exception as e:
        logging.exception(e)
        raise PreventUpdate from e


def get_position(figure: dict[str, list[dict]]) -> tuple[list | None, list | None]:
    node = figure["data"][0].get("node")
    x_state, y_state = (node.get("x"), node.get("y")) if node else (None, None)

    return x_state, y_state
