import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from stf.dependency_configurator import services
from stf.domain import SankeyDTO

app = FastAPI()


@app.post("/api/sankey", response_class=HTMLResponse)
async def post_sankey_data(dto: SankeyDTO) -> str:
    return services.chart_service().get_sankey_html_from_dto(dto)


def start() -> None:
    uvicorn.run("stf.entrypoints.api:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
