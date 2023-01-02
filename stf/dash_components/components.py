import pandas as pd
from dash import dash_table, html, dcc
from dash.development.base_component import Component

default_figure = {"data": [{"type": "sankey"}]}
sankey_graph = dcc.Graph(className="chart", id="snk-graph", figure=default_figure)
width_input = dcc.Input(className="input", id="snk-width", type="number", placeholder="1920px")
height_input = dcc.Input(className="input", id="snk-height", type="number", placeholder="1080px")
font_size_input = dcc.Input(className="input", id="snk-font-size", type="number", placeholder="12", value=20)
node_pad_input = dcc.Input(className="input", id="snk-node-pad", type="number", placeholder="20px", value=18)
node_thickness_input = dcc.Input(
    className="input", id="snk-node-thickness", type="number", placeholder="20px", value=10
)
unit_input = dcc.Input(className="input", id="snk-unit", type="text", placeholder="€")
show_amout_check = dcc.Checklist(className="check-list", id="snk-full-label", inline=True, options=["Show amounts"])
color_dropdown = dcc.Dropdown(
    className="dropdown",
    id="snk-colorscales",
    options=["IceFire", "Twilight", "HSV", "mrybm", "mygbm", "Edge"],
    value="IceFire",
    clearable=False,
)

dummy_data = pd.read_csv("datasets/sample.csv")
add_row_button = html.Button("Add Row", className="button", id="add-rows-button", n_clicks=0)
file_alert = dcc.ConfirmDialog(message="...", id="alert", displayed=False)
upload_box = dcc.Upload(
    className="upload-box", id="upload-data", children=html.Div(["Drag and Drop or ", html.A("Select Files")])
)
input_table = dash_table.DataTable(
    id="snk-links",
    columns=[
        {"name": "Source", "id": "source", "type": "text"},
        {"name": "Amount", "id": "amount", "type": "numeric"},
        {"name": "Target", "id": "target", "type": "text"},
    ],
    data=dummy_data.to_dict("records"),
    editable=True,
    row_deletable=True,
)


def add_label(component: Component, label: str, class_name: str = "") -> Component:
    return html.Div(children=[html.P(className=class_name, children=label), component])
