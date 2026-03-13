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

    # Порядок как в backend-clone: X-Forwarded-For (цепочка прокси), X-Real-IP, CF-Connecting-IP
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    elif request.headers.get("x-real-ip"):
        client_ip = request.headers.get("x-real-ip")
    elif request.headers.get("cf-connecting-ip"):
        client_ip = request.headers.get("cf-connecting-ip")
    else:
        client_ip = request.client.host if request.client else "unknown"

    asyncio.create_task(
        _log_click_safe(
            url_id=url_data["url_id"],
            short_code=short_code,
            ip_address=client_ip,
            user_agent=request.headers.get("user-agent", ""),
            referrer=request.headers.get("referer", ""),
            country=lookup_country(client_ip),
        )
    )

    return RedirectResponse(
        url=url_data["original_url"],
        status_code=status.HTTP_302_FOUND,
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


async def _log_click_safe(**kwargs) -> None:
    try:
        await log_click(**kwargs)
    except Exception:
        logger.exception("Failed to log click")
