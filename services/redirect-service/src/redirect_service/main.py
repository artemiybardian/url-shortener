import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from redirect_service.cache import close_redis
from redirect_service.router import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await close_redis()
    logger.info("Redis connection closed")


app = FastAPI(
    title="Redirect Service",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)
