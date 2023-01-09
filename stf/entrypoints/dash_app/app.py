from dash import Dash
from stf.entrypoints.dash_app.pages.sankey_graph import layout

app = Dash(__name__, assets_folder="../../../assets")
app.layout = layout


def start() -> None:
    app.run()


if __name__ == "__main__":
    start()
