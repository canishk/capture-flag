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
        json={"name": "Web", "icon": "shield"},
    )
    category_id = category.json()["data"]["id"]
    level = await client.post(
        "/api/v1/levels",
        headers=headers,
        json={"categoryId": category_id, "name": "Basics"},
    )
    level_id = level.json()["data"]["id"]
    challenge = await client.post(
        "/api/v1/challenges",
        headers=headers,
        json={
            "categoryId": category_id,
            "levelId": level_id,
            "title": "SQLi 101",
            "description": "Find the flag",
            "objectives": ["Understand SQLi"],
            "challengeType": "text_answer",
            "baseScore": 100,
            "evaluationStrategy": {
                "type": "exact_match",
                "expectedAnswer": "flag{test}",
            },
        },
    )
    challenge_id = challenge.json()["data"]["id"]
    await client.post(f"/api/v1/challenges/{challenge_id}/publish", headers=headers)
    return challenge_id


@pytest.mark.asyncio
async def test_submission_evaluates_and_updates_progress(
    client: AsyncClient, session_factory, registered_user: dict
) -> None:
    await _promote_admin(session_factory, registered_user["user_id"])
    headers = {"Authorization": f"Bearer {registered_user['tokens']['accessToken']}"}
    challenge_id = await _seed_published_challenge(client, headers)

    wrong = await client.post(
        "/api/v1/submissions",
        headers=headers,
        json={"challengeId": challenge_id, "answer": "wrong"},
    )
    assert wrong.status_code == 201
    assert wrong.json()["data"]["status"] == "failed"
    assert wrong.json()["data"]["attemptNumber"] == 1

    correct = await client.post(
        "/api/v1/submissions",
        headers=headers,
        json={"challengeId": challenge_id, "answer": "flag{test}"},
    )
    assert correct.status_code == 201
    assert correct.json()["data"]["status"] == "passed"
    assert correct.json()["data"]["attemptNumber"] == 2

    progress = await client.get("/api/v1/progress/me", headers=headers)
    assert progress.status_code == 200
    body = progress.json()["data"]
    assert body["challengesAttempted"] == 2
    assert body["challengesCompleted"] == 1
    assert body["totalXp"] == 100
