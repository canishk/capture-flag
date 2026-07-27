from uuid import UUID

import pytest
from httpx import AsyncClient

from app.modules.users.domain.enums import UserRole
from app.modules.users.infrastructure.repository import UserRepository


async def _promote_admin(session_factory, user_id: str) -> None:
    async with session_factory() as session:
        await UserRepository(session).update_role(UUID(user_id), UserRole.ADMINISTRATOR)
        await session.commit()


async def _seed_published_challenge(client: AsyncClient, headers: dict) -> str:
    category = await client.post(
        "/api/v1/categories",
        headers=headers,
        json={"name": "Crypto", "icon": "key"},
    )
    category_id = category.json()["data"]["id"]
    level = await client.post(
        "/api/v1/levels",
        headers=headers,
        json={"categoryId": category_id, "name": "Intro"},
    )
    level_id = level.json()["data"]["id"]
    challenge = await client.post(
        "/api/v1/challenges",
        headers=headers,
        json={
            "categoryId": category_id,
            "levelId": level_id,
            "title": "Hash Basics",
            "description": "Learn hashing",
            "objectives": ["Understand hashes"],
            "challengeType": "text_answer",
            "baseScore": 100,
            "evaluationStrategy": {"type": "exact_match"},
        },
    )
    challenge_id = challenge.json()["data"]["id"]
    await client.post(f"/api/v1/challenges/{challenge_id}/publish", headers=headers)
    return challenge_id


@pytest.mark.asyncio
async def test_create_publish_hint_for_challenge(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    challenge_id = await _seed_published_challenge(client, headers)

    created = await client.post(
        "/api/v1/hints",
        headers=headers,
        json={
            "challengeId": challenge_id,
            "title": "Nudge",
            "content": "Think about one-way functions",
        },
    )
    assert created.status_code == 201
    hint_id = created.json()["data"]["id"]

    published = await client.post(f"/api/v1/hints/{hint_id}/publish", headers=headers)
    assert published.status_code == 200

    listed = await client.get(f"/api/v1/hints/challenge/{challenge_id}")
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] == 1


@pytest.mark.asyncio
async def test_create_link_resource_to_challenge(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    challenge_id = await _seed_published_challenge(client, headers)

    created = await client.post(
        "/api/v1/resources",
        headers=headers,
        json={
            "title": "OWASP Hashing",
            "resourceType": "article",
            "url": "https://owasp.org/example",
        },
    )
    assert created.status_code == 201
    resource_id = created.json()["data"]["id"]
    await client.post(f"/api/v1/resources/{resource_id}/publish", headers=headers)

    linked = await client.post(
        f"/api/v1/resources/{resource_id}/link",
        headers=headers,
        json={"challengeId": challenge_id},
    )
    assert linked.status_code == 200

    listed = await client.get(f"/api/v1/resources/challenge/{challenge_id}")
    assert listed.status_code == 200
    assert listed.json()["meta"]["totalItems"] == 1
