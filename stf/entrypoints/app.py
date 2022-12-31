import uvicorn
from dash import html
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.wsgi import WSGIMiddleware
from stf.dash_components import app as dash_app, sidebar, main_panel
from stf.sankey import Sankey
from stf.dto import SankeyDTO

app = FastAPI()
dash_app.layout = html.Div(className="container", children=[sidebar, main_panel])
app.mount("/", WSGIMiddleware(dash_app.server))


@app.post("/api/links", response_class=HTMLResponse)
def read_main(dto: SankeyDTO) -> str:
    sankey = Sankey.from_dto(dto)
    return sankey.get_html()


def start() -> None:
    uvicorn.run("stf:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
