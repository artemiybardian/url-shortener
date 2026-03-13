import json
import logging

from redis.asyncio import Redis

from redirect_service.config import settings

logger = logging.getLogger(__name__)

CACHE_TTL = 300  # 5 minutes

_redis: Redis | None = None


async def get_redis() -> Redis:
    global _redis  # noqa: PLW0603
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis


async def close_redis() -> None:
    global _redis  # noqa: PLW0603
    if _redis is not None:
        await _redis.close()
        _redis = None


def _key(short_code: str) -> str:
    return f"redirect:{short_code}"


async def get_cached_url(short_code: str) -> dict | None:
    r = await get_redis()
    data = await r.get(_key(short_code))
    if data is None:
        return None
    return json.loads(data)


async def set_cached_url(short_code: str, url_data: dict) -> None:
    r = await get_redis()
    await r.set(_key(short_code), json.dumps(url_data), ex=CACHE_TTL)
