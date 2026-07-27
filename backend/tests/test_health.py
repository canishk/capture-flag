import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_live_endpoint(client: AsyncClient) -> None:
    response = await client.get("/api/v1/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"
