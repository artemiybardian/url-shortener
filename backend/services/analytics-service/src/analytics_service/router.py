from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from analytics_service.database import get_session
from analytics_service.service import get_url_stats

router = APIRouter()


@router.get("/{short_code}/stats")
async def stats(
    short_code: str,
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    return await get_url_stats(session, short_code)
