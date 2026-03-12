import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    resp = await client.post("/register", json={"email": "user@test.com", "password": "secret123"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "user@test.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "secret123"}
    await client.post("/register", json=payload)
    resp = await client.post("/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/register", json={"email": "login@test.com", "password": "pass123"})
    resp = await client.post("/login", json={"email": "login@test.com", "password": "pass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"  # noqa: S105


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/register", json={"email": "wrong@test.com", "password": "correct"})
    resp = await client.post("/login", json={"email": "wrong@test.com", "password": "incorrect"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client):
    resp = await client.post("/login", json={"email": "ghost@test.com", "password": "whatever"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client):
    await client.post("/register", json={"email": "refresh@test.com", "password": "pass123"})
    login_resp = await client.post("/login", json={"email": "refresh@test.com", "password": "pass123"})
    refresh_token = login_resp.json()["refresh_token"]

    resp = await client.post("/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_with_access_token_fails(client):
    await client.post("/register", json={"email": "bad@test.com", "password": "pass123"})
    login_resp = await client.post("/login", json={"email": "bad@test.com", "password": "pass123"})
    access_token = login_resp.json()["access_token"]

    resp = await client.post("/refresh", json={"refresh_token": access_token})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me_authenticated(client):
    await client.post("/register", json={"email": "me@test.com", "password": "pass123"})
    login_resp = await client.post("/login", json={"email": "me@test.com", "password": "pass123"})
    token = login_resp.json()["access_token"]

    resp = await client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "me@test.com"


@pytest.mark.asyncio
async def test_me_no_token(client):
    resp = await client.get("/me")
    assert resp.status_code == 401
