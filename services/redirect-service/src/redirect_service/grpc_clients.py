import grpc

from redirect_service.config import settings
from shared.proto import analytics_pb2, analytics_pb2_grpc, shortener_pb2, shortener_pb2_grpc


async def resolve_url(short_code: str) -> dict | None:
    """Call shortener-service gRPC to resolve a short code."""
    async with grpc.aio.insecure_channel(settings.shortener_grpc_address) as channel:
        stub = shortener_pb2_grpc.ShortenerServiceStub(channel)
        try:
            resp = await stub.ResolveURL(shortener_pb2.ResolveRequest(short_code=short_code))
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise
    return {
        "original_url": resp.original_url,
        "url_id": resp.url_id,
        "is_active": resp.is_active,
    }


async def log_click(
    url_id: str,
    short_code: str,
    ip_address: str,
    user_agent: str = "",
    referrer: str = "",
    country: str = "",
) -> None:
    """Fire-and-forget click logging via analytics-service gRPC."""
    async with grpc.aio.insecure_channel(settings.analytics_grpc_address) as channel:
        stub = analytics_pb2_grpc.AnalyticsServiceStub(channel)
        await stub.LogClick(analytics_pb2.ClickEvent(
            url_id=url_id,
            short_code=short_code,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            country=country,
        ))
