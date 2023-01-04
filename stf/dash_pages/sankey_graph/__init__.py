from dash import html
from stf.dash_pages.sankey_graph.sidebar import sidebar
from stf.dash_pages.sankey_graph.main_panel import main_panel

layout = html.Div(className="container", children=[sidebar, main_panel])
