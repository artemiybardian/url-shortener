import logging
from contextlib import asynccontextmanager

import grpc
from fastapi import FastAPI

from shared.proto import shortener_pb2_grpc
from shortener_service.config import settings
from shortener_service.grpc_server import ShortenerGRPCServicer
from shortener_service.router import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    grpc_server = grpc.aio.server()
    shortener_pb2_grpc.add_ShortenerServiceServicer_to_server(ShortenerGRPCServicer(), grpc_server)
    listen_addr = f"[::]:{settings.shortener_grpc_port}"
    grpc_server.add_insecure_port(listen_addr)
    await grpc_server.start()
    logger.info("gRPC server started on %s", listen_addr)

    yield

    await grpc_server.stop(grace=5)
    logger.info("gRPC server stopped")


app = FastAPI(
    title="Shortener Service",
    version="0.1.0",
    root_path="/api/urls",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
