import secrets
import string
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shortener_service.models import URL

CODE_ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 7


def _generate_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))


async def get_url_by_code(session: AsyncSession, short_code: str) -> URL | None:
    result = await session.execute(select(URL).where(URL.short_code == short_code))
    return result.scalar_one_or_none()


async def create_short_url(
    session: AsyncSession,
    original_url: str,
    user_id: uuid.UUID | None = None,
    custom_code: str | None = None,
) -> URL:
    code = custom_code or _generate_code()

    existing = await get_url_by_code(session, code)
    if existing:
        if custom_code:
            msg = f"Code '{code}' is already taken"
            raise ValueError(msg)
        # collision on random code — retry once
        code = _generate_code()

    url = URL(short_code=code, original_url=original_url, user_id=user_id)
    session.add(url)
    await session.commit()
    await session.refresh(url)
    return url


async def list_user_urls(session: AsyncSession, user_id: uuid.UUID) -> list[URL]:
    result = await session.execute(select(URL).where(URL.user_id == user_id).order_by(URL.created_at.desc()))
    return list(result.scalars().all())


async def deactivate_url(session: AsyncSession, short_code: str, user_id: uuid.UUID) -> URL | None:
    url = await get_url_by_code(session, short_code)
    if url is None or url.user_id != user_id:
        return None
    url.is_active = False
    await session.commit()
    await session.refresh(url)
    return url
