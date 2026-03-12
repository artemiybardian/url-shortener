import pytest

from analytics_service.models import Click


@pytest.mark.asyncio
async def test_stats_empty(client):
    resp = await client.get("/abc123/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["short_code"] == "abc123"
    assert data["total_clicks"] == 0
    assert data["top_referrers"] == []
    assert data["recent_clicks"] == []


@pytest.mark.asyncio
async def test_stats_with_clicks(client, session):
    for i in range(3):
        session.add(Click(
            url_id="url-1",
            short_code="xyz",
            ip_address=f"1.2.3.{i}",
            user_agent="TestBot/1.0",
            referrer="https://google.com" if i < 2 else "",
        ))
    await session.commit()

    resp = await client.get("/xyz/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_clicks"] == 3
    assert len(data["recent_clicks"]) == 3
    assert data["top_referrers"][0]["referrer"] == "https://google.com"
    assert data["top_referrers"][0]["count"] == 2


@pytest.mark.asyncio
async def test_stats_recent_clicks_limit(client, session):
    for i in range(25):
        session.add(Click(
            url_id="url-2",
            short_code="many",
            ip_address=f"10.0.0.{i}",
        ))
    await session.commit()

    resp = await client.get("/many/stats")
    data = resp.json()
    assert data["total_clicks"] == 25
    assert len(data["recent_clicks"]) == 20
