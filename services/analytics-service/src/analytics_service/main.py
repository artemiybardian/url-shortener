import logging
from contextlib import asynccontextmanager

import grpc
from fastapi import FastAPI

from analytics_service.config import settings
from analytics_service.grpc_server import AnalyticsGRPCServicer
from analytics_service.router import router
from shared.proto import analytics_pb2_grpc

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    grpc_server = grpc.aio.server()
    analytics_pb2_grpc.add_AnalyticsServiceServicer_to_server(AnalyticsGRPCServicer(), grpc_server)
    listen_addr = f"[::]:{settings.analytics_grpc_port}"
    grpc_server.add_insecure_port(listen_addr)
    await grpc_server.start()
    logger.info("gRPC server started on %s", listen_addr)

    yield

    await grpc_server.stop(grace=5)
    logger.info("gRPC server stopped")


app = FastAPI(
    title="Analytics Service",
    version="0.1.0",
    root_path="/api/analytics",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
