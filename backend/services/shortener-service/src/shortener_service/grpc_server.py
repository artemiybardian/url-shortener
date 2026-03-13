import asyncio
import logging

import grpc
from sqlalchemy import select

from shared.proto import shortener_pb2, shortener_pb2_grpc
from shortener_service.config import settings
from shortener_service.database import async_session
from shortener_service.models import URL

logger = logging.getLogger(__name__)


class ShortenerGRPCServicer(shortener_pb2_grpc.ShortenerServiceServicer):
    async def ResolveURL(self, request, context):  # noqa: N802
        async with async_session() as session:
            result = await session.execute(select(URL).where(URL.short_code == request.short_code))
            url = result.scalar_one_or_none()

        if url is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "Short code not found")

        return shortener_pb2.ResolveResponse(
            original_url=url.original_url,
            url_id=str(url.id),
            is_active=url.is_active,
        )


async def serve() -> None:
    server = grpc.aio.server()
    shortener_pb2_grpc.add_ShortenerServiceServicer_to_server(ShortenerGRPCServicer(), server)
    listen_addr = f"[::]:{settings.shortener_grpc_port}"
    server.add_insecure_port(listen_addr)
    logger.info("gRPC server starting on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
