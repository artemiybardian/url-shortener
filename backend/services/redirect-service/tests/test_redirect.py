from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_redirect_success(client, mock_resolve_url, mock_log_click, mock_cache):  # noqa: ARG001
    mock_resolve_url.return_value = {
        "original_url": "https://example.com",
        "url_id": "uuid-123",
        "is_active": True,
    }

    resp = await client.get("/abc123")
    assert resp.status_code == 302
    assert resp.headers["location"] == "https://example.com"
    mock_resolve_url.assert_awaited_once_with("abc123")


@pytest.mark.asyncio
async def test_redirect_not_found(client, mock_resolve_url, mock_log_click, mock_cache):  # noqa: ARG001
    mock_resolve_url.return_value = None

    resp = await client.get("/nope")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_redirect_deactivated(client, mock_resolve_url, mock_log_click, mock_cache):  # noqa: ARG001
    mock_resolve_url.return_value = {
        "original_url": "https://example.com",
        "url_id": "uuid-123",
        "is_active": False,
    }

    resp = await client.get("/dead")
    assert resp.status_code == 410


@pytest.mark.asyncio
async def test_redirect_uses_cache(client, mock_resolve_url, mock_log_click):  # noqa: ARG001
    cached = {
        "original_url": "https://cached.com",
        "url_id": "uuid-cached",
        "is_active": True,
    }

    with (
        patch("redirect_service.router.get_cached_url", new_callable=AsyncMock, return_value=cached),
        patch("redirect_service.router.set_cached_url", new_callable=AsyncMock) as mock_set,
    ):
        resp = await client.get("/cached")
        assert resp.status_code == 302
        assert resp.headers["location"] == "https://cached.com"
        mock_resolve_url.assert_not_awaited()
        mock_set.assert_not_awaited()


@pytest.mark.asyncio
async def test_health_endpoint(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
