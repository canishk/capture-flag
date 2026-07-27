from uuid import UUID

import pytest
from httpx import AsyncClient

from app.modules.users.domain.enums import UserRole
from app.modules.users.infrastructure.repository import UserRepository


async def _promote_admin(session_factory, user_id: str) -> None:
    async with session_factory() as session:
        await UserRepository(session).update_role(UUID(user_id), UserRole.ADMINISTRATOR)
        await session.commit()


@pytest.mark.asyncio
async def test_create_level_under_category(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}

    category = await client.post(
        "/api/v1/categories",
        headers=headers,
        json={"name": "Linux", "icon": "terminal"},
    )
    category_id = category.json()["data"]["id"]

    level = await client.post(
        "/api/v1/levels",
        headers=headers,
        json={
            "categoryId": category_id,
            "name": "Foundations",
            "description": "Basics",
        },
    )
    assert level.status_code == 201
    assert level.json()["data"]["categoryId"] == category_id

    listed = await client.get(f"/api/v1/levels?categoryId={category_id}")
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] == 1
