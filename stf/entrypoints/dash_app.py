from dash import Dash, html
from stf.dash_components import sidebar, main_panel

app = Dash(__name__, assets_folder="../../assets")
app.layout = html.Div(className="container", children=[sidebar, main_panel])


def start() -> None:
    app.run()


if __name__ == "__main__":
    start()
