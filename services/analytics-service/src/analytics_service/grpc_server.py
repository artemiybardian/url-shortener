import logging

import grpc

from analytics_service.database import async_session
from analytics_service.models import Click
from shared.proto import analytics_pb2, analytics_pb2_grpc

logger = logging.getLogger(__name__)


class AnalyticsGRPCServicer(analytics_pb2_grpc.AnalyticsServiceServicer):
    async def LogClick(self, request, context):  # noqa: N802
        click = Click(
            url_id=request.url_id,
            short_code=request.short_code,
            ip_address=request.ip_address,
            user_agent=request.user_agent,
            referrer=request.referrer,
        )
        try:
            async with async_session() as session:
                session.add(click)
                await session.commit()
        except Exception:
            logger.exception("Failed to log click for %s", request.short_code)
            return analytics_pb2.LogResponse(success=False)

        return analytics_pb2.LogResponse(success=True)
