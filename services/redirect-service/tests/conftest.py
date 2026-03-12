from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from redirect_service.main import app


@pytest.fixture
def mock_resolve_url():
    with patch("redirect_service.router.resolve_url", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_log_click():
    with patch("redirect_service.router.log_click", new_callable=AsyncMock) as mock:
        yield mock


@pytest.fixture
def mock_cache():
    with (
        patch("redirect_service.router.get_cached_url", new_callable=AsyncMock, return_value=None) as mock_get,
        patch("redirect_service.router.set_cached_url", new_callable=AsyncMock) as mock_set,
    ):
        yield mock_get, mock_set


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=False,
    ) as ac:
        yield ac
