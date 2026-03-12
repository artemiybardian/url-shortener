import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from shortener_service.config import settings
from shortener_service.database import get_session
from shortener_service.schemas import URLCreate, URLResponse
from shortener_service.service import create_short_url, deactivate_url, list_user_urls
from shared.dependencies import require_auth

router = APIRouter()

get_current_user = require_auth(settings.jwt_secret_key, settings.jwt_algorithm)


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_url(
    body: URLCreate,
    current_user: dict = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    try:
        url = await create_short_url(
            session,
            str(body.original_url),
            uuid.UUID(current_user["sub"]),
            body.custom_code,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
    return url


@router.get("/", response_model=list[URLResponse])
async def list_urls(
    current_user: dict = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    return await list_user_urls(session, uuid.UUID(current_user["sub"]))


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    short_code: str,
    current_user: dict = Depends(get_current_user),  # noqa: B008
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    url = await deactivate_url(session, short_code, uuid.UUID(current_user["sub"]))
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
