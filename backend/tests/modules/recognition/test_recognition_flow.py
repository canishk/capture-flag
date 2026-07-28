from uuid import UUID

import pytest
from httpx import AsyncClient

from app.modules.users.domain.enums import UserRole
from app.modules.users.infrastructure.repository import UserRepository


async def _promote_admin(session_factory, user_id: str) -> None:
    async with session_factory() as session:
        await UserRepository(session).update_role(UUID(user_id), UserRole.ADMINISTRATOR)
        await session.commit()


async def _seed_challenge(client: AsyncClient, headers: dict) -> str:
    category = await client.post(
        "/api/v1/categories", headers=headers, json={"name": "Crypto", "icon": "key"}
    )
    category_id = category.json()["data"]["id"]
    level = await client.post(
        "/api/v1/levels", headers=headers, json={"categoryId": category_id, "name": "Intro"}
    )
    level_id = level.json()["data"]["id"]
    challenge = await client.post(
        "/api/v1/challenges",
        headers=headers,
        json={
            "categoryId": category_id,
            "levelId": level_id,
            "title": "Hash Hunt",
            "description": "Find flag",
            "objectives": ["Learn hashing"],
            "challengeType": "text_answer",
            "baseScore": 100,
            "evaluationStrategy": {"type": "exact_match", "expectedAnswer": "flag{win}"},
        },
    )
    challenge_id = challenge.json()["data"]["id"]
    await client.post(f"/api/v1/challenges/{challenge_id}/publish", headers=headers)
    return challenge_id


@pytest.mark.asyncio
async def test_recognition_flow_awards_trophy_and_updates_leaderboard(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}

    await client.post(
        "/api/v1/trophies",
        headers=headers,
        json={
            "code": "first_challenge",
            "name": "First Steps",
            "description": "Complete your first challenge",
            "icon": "star",
            "triggerType": "first_challenge",
        },
    )
    await client.post(
        "/api/v1/achievements",
        headers=headers,
        json={
            "code": "challenge_starter",
            "name": "Challenge Starter",
            "description": "Complete one challenge",
            "icon": "badge",
            "criteriaType": "challenge_count",
            "targetCount": 1,
        },
    )

    challenge_id = await _seed_challenge(client, headers)
    submit = await client.post(
        "/api/v1/submissions",
        headers=headers,
        json={"challengeId": challenge_id, "answer": "flag{win}"},
    )
    assert submit.status_code == 201

    trophies = await client.get("/api/v1/trophies/me", headers=headers)
    assert trophies.status_code == 200
    assert trophies.json()["meta"]["totalItems"] >= 1

    achievements = await client.get("/api/v1/achievements/me", headers=headers)
    assert achievements.status_code == 200
    assert achievements.json()["meta"]["totalItems"] >= 1

    leaderboard = await client.get("/api/v1/leaderboards/me", headers=headers)
    assert leaderboard.status_code == 200
    assert leaderboard.json()["data"]["xp"] == 100
