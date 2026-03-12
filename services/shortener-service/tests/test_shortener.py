import pytest


@pytest.mark.asyncio
async def test_create_url(client, auth_headers):
    resp = await client.post("/", json={"original_url": "https://example.com"}, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["original_url"] == "https://example.com/"
    assert data["is_active"] is True
    assert len(data["short_code"]) == 7


@pytest.mark.asyncio
async def test_create_url_custom_code(client, auth_headers):
    resp = await client.post(
        "/", json={"original_url": "https://example.com", "custom_code": "mylink"}, headers=auth_headers
    )
    assert resp.status_code == 201
    assert resp.json()["short_code"] == "mylink"


@pytest.mark.asyncio
async def test_create_url_duplicate_custom_code(client, auth_headers):
    payload = {"original_url": "https://example.com", "custom_code": "taken"}
    await client.post("/", json=payload, headers=auth_headers)
    resp = await client.post("/", json=payload, headers=auth_headers)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_list_urls(client, auth_headers):
    await client.post("/", json={"original_url": "https://a.com"}, headers=auth_headers)
    await client.post("/", json={"original_url": "https://b.com"}, headers=auth_headers)

    resp = await client.get("/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
async def test_delete_url(client, auth_headers):
    create_resp = await client.post("/", json={"original_url": "https://del.com"}, headers=auth_headers)
    code = create_resp.json()["short_code"]

    resp = await client.delete(f"/{code}", headers=auth_headers)
    assert resp.status_code == 204

    urls = (await client.get("/", headers=auth_headers)).json()
    assert urls[0]["is_active"] is False


@pytest.mark.asyncio
async def test_delete_nonexistent_url(client, auth_headers):
    resp = await client.delete("/nope123", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_create_url_no_auth(client):
    resp = await client.post("/", json={"original_url": "https://example.com"})
    assert resp.status_code == 401
