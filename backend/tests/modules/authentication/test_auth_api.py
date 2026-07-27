import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_and_me(client: AsyncClient) -> None:
    register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "password": "password123",
            "displayName": "Alice",
        },
    )
    assert register.status_code == 201
    register_body = register.json()
    assert register_body["success"] is True
    assert register_body["data"]["tokens"]["accessToken"]

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    tokens = login.json()["data"]
    headers = {"Authorization": f"Bearer {tokens['accessToken']}"}

    me = await client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_conflict(client: AsyncClient) -> None:
    payload = {
        "email": "dup@example.com",
        "password": "password123",
        "displayName": "Dup",
    }
    first = await client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201
    second = await client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "EMAIL_ALREADY_REGISTERED"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient, registered_user: dict) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_refresh_token_rotation(client: AsyncClient, registered_user: dict) -> None:
    refresh_token = registered_user["tokens"]["refreshToken"]
    refreshed = await client.post(
        "/api/v1/auth/refresh",
        json={"refreshToken": refresh_token},
    )
    assert refreshed.status_code == 200
    new_tokens = refreshed.json()["data"]

    replay = await client.post(
        "/api/v1/auth/refresh",
        json={"refreshToken": refresh_token},
    )
    assert replay.status_code == 401

    headers = {"Authorization": f"Bearer {new_tokens['accessToken']}"}
    me = await client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200


@pytest.mark.asyncio
async def test_change_password_revokes_old_refresh(client: AsyncClient, registered_user: dict) -> None:
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    changed = await client.post(
        "/api/v1/auth/change-password",
        headers=headers,
        json={"currentPassword": "password123", "newPassword": "newpassword123"},
    )
    assert changed.status_code == 200

    old_refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refreshToken": registered_user["tokens"]["refreshToken"]},
    )
    assert old_refresh.status_code == 401

    login = await client.post(
        "/api/v1/auth/login",
        json={"email": registered_user["email"], "password": "newpassword123"},
    )
    assert login.status_code == 200
