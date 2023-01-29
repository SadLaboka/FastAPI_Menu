import aioredis
import uvicorn
from fastapi import FastAPI

from src.api.v1.routes import menus
from src.core import config
from src.db import cache

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
    cache.cache = await aioredis.from_url(config.REDIS_URL)


@app.on_event("shutdown")
async def shutdown():
    await cache.cache.close()


app.include_router(router=menus.router, prefix="/api/v1/menus")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
