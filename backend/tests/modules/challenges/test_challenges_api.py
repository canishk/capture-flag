from uuid import UUID

import pytest
from httpx import AsyncClient

from app.modules.users.domain.enums import UserRole
from app.modules.users.infrastructure.repository import UserRepository


async def _promote_admin(session_factory, user_id: str) -> None:
    async with session_factory() as session:
        await UserRepository(session).update_role(UUID(user_id), UserRole.ADMINISTRATOR)
        await session.commit()


async def _seed_category_level(client: AsyncClient, headers: dict) -> tuple[str, str]:
    category = await client.post(
        "/api/v1/categories",
        headers=headers,
        json={"name": "Web Security", "icon": "shield"},
    )
    category_id = category.json()["data"]["id"]
    level = await client.post(
        "/api/v1/levels",
        headers=headers,
        json={"categoryId": category_id, "name": "Basics"},
    )
    return category_id, level.json()["data"]["id"]


@pytest.mark.asyncio
async def test_create_publish_and_list_challenge(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    category_id, level_id = await _seed_category_level(client, headers)

    created = await client.post(
        "/api/v1/challenges",
        headers=headers,
        json={
            "categoryId": category_id,
            "levelId": level_id,
            "title": "SQL Injection Basics",
            "description": "Learn SQL injection fundamentals",
            "objectives": ["Understand SQL injection", "Identify vulnerable queries"],
            "challengeType": "text_answer",
            "baseScore": 100,
            "evaluationStrategy": {"type": "exact_match", "answer": "flag{test}"},
        },
    )
    assert created.status_code == 201
    challenge_id = created.json()["data"]["id"]
    assert created.json()["data"]["status"] == "draft"

    published = await client.post(
        f"/api/v1/challenges/{challenge_id}/publish",
        headers=headers,
    )
    assert published.status_code == 200
    assert published.json()["data"]["status"] == "published"

    listed = await client.get("/api/v1/challenges")
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] == 1


@pytest.mark.asyncio
async def test_learner_cannot_see_draft_challenge(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    category_id, level_id = await _seed_category_level(client, headers)

    created = await client.post(
        "/api/v1/challenges",
        headers=headers,
        json={
            "categoryId": category_id,
            "levelId": level_id,
            "title": "Hidden Draft",
            "description": "Draft only",
            "objectives": ["Test visibility"],
            "challengeType": "text_answer",
            "baseScore": 50,
            "evaluationStrategy": {"type": "exact_match"},
        },
    )
    challenge_id = created.json()["data"]["id"]

    hidden = await client.get(f"/api/v1/challenges/{challenge_id}")
    assert hidden.status_code == 404
