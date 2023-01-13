from typing import Optional

import uvicorn
from fastapi import FastAPI as FastAPIApplication

from src.core import config
from src.db import Database


class FastAPI(FastAPIApplication):
    database: Optional[Database] = None


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


@app.on_event("startup")
async def startup():
    app.database = Database()
    await app.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await app.database.disconnect()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )
