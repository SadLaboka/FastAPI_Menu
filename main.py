import uvicorn
from fastapi import FastAPI

from src.core import config

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


@app.get("/")
def root():
    return {"service": config.PROJECT_NAME, "version": config.VERSION}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
