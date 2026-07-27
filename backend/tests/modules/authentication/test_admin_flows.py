from uuid import UUID

import pytest
from httpx import AsyncClient

from app.modules.users.domain.enums import UserRole
from app.modules.users.infrastructure.repository import UserRepository


@pytest.mark.asyncio
async def test_admin_can_list_and_disable_users(
    client: AsyncClient,
    session_factory,
    registered_user: dict,
) -> None:
    async with session_factory() as session:
        repo = UserRepository(session)
        await repo.update_role(UUID(registered_user["user_id"]), UserRole.ADMINISTRATOR)
        await session.commit()

    admin_headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}

    listed = await client.get("/api/v1/users", headers=admin_headers)
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] >= 1

    disabled = await client.post(
        f"/api/v1/users/{registered_user['user_id']}/disable",
        headers=admin_headers,
    )
    assert disabled.status_code == 200
    assert disabled.json()["data"]["status"] == "disabled"


@pytest.mark.asyncio
async def test_reset_password_rejects_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/reset-password",
        json={"token": "invalid-token-value", "newPassword": "anotherpass123"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_TOKEN"
