import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_and_update_profile(client: AsyncClient, registered_user: dict) -> None:
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    profile = await client.get("/api/v1/users/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["data"]["displayName"] == "Learner One"

    updated = await client.patch(
        "/api/v1/users/me",
        headers=headers,
        json={"displayName": "Updated Name", "preferences": {"theme": "dark"}},
    )
    assert updated.status_code == 200
    body = updated.json()["data"]
    assert body["displayName"] == "Updated Name"
    assert body["preferences"]["theme"] == "dark"


@pytest.mark.asyncio
async def test_public_profile_endpoint(client: AsyncClient, registered_user: dict) -> None:
    response = await client.get(f"/api/v1/users/{registered_user['user_id']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["displayName"] == "Learner One"
    assert "email" not in data


@pytest.mark.asyncio
async def test_admin_list_users_requires_admin(client: AsyncClient, registered_user: dict) -> None:
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    response = await client.get("/api/v1/users", headers=headers)
    assert response.status_code == 403
