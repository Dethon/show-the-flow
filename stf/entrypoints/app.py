import uvicorn
from fastapi.middleware.wsgi import WSGIMiddleware
from stf.entrypoints.dash_app.app import app as dash_app
from stf.entrypoints.api import app


app.mount("/", WSGIMiddleware(dash_app.server))


def start() -> None:
    uvicorn.run("stf.entrypoints.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
