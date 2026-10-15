from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .routes import router

app = FastAPI(title="Book Tracker API")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}


Instrumentator().instrument(app).expose(app)