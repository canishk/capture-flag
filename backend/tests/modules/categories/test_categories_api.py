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
async def test_admin_create_and_list_categories(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}

    created = await client.post(
        "/api/v1/categories",
        headers=headers,
        json={
            "name": "Web Security",
            "description": "Learn web app security",
            "icon": "shield",
        },
    )
    assert created.status_code == 201
    body = created.json()["data"]
    assert body["name"] == "Web Security"
    assert body["status"] == "active"

    listed = await client.get("/api/v1/categories", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] >= 1


@pytest.mark.asyncio
async def test_learner_cannot_see_hidden_category(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}

    created = await client.post(
        "/api/v1/categories",
        headers=headers,
        json={"name": "Hidden Topic", "icon": "lock"},
    )
    category_id = created.json()["data"]["id"]
    await client.delete(f"/api/v1/categories/{category_id}", headers=headers)

    hidden_get = await client.get(f"/api/v1/categories/{category_id}")
    assert hidden_get.status_code == 404


@pytest.mark.asyncio
async def test_duplicate_category_name_conflict(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    payload = {"name": "Cryptography", "icon": "key"}

    first = await client.post("/api/v1/categories", headers=headers, json=payload)
    assert first.status_code == 201
    second = await client.post("/api/v1/categories", headers=headers, json=payload)
    assert second.status_code == 409
