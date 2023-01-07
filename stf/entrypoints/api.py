import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from stf.domain import Sankey, SankeyDTO

app = FastAPI()


@app.post("/api/links", response_class=HTMLResponse)
def read_main(dto: SankeyDTO) -> str:
    sankey = Sankey.from_dto(dto)
    return sankey.get_html()


def start() -> None:
    uvicorn.run("stf.entrypoints.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
