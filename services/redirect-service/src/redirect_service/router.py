import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from redirect_service.cache import get_cached_url, set_cached_url
from redirect_service.geo import lookup_country
from redirect_service.grpc_clients import log_click, resolve_url

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{short_code}")
async def redirect(short_code: str, request: Request):
    url_data = await get_cached_url(short_code)

    if url_data is None:
        url_data = await resolve_url(short_code)
        if url_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
        await set_cached_url(short_code, url_data)

    if not url_data["is_active"]:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="This link has been deactivated")

    client_ip = request.client.host if request.client else "unknown"

    asyncio.create_task(_log_click_safe(
        url_id=url_data["url_id"],
        short_code=short_code,
        ip_address=client_ip,
        user_agent=request.headers.get("user-agent", ""),
        referrer=request.headers.get("referer", ""),
        country=lookup_country(client_ip),
    ))

    return RedirectResponse(url=url_data["original_url"], status_code=status.HTTP_301_MOVED_PERMANENTLY)


async def _log_click_safe(**kwargs) -> None:
    try:
        await log_click(**kwargs)
    except Exception:
        logger.exception("Failed to log click")
