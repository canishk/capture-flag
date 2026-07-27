import pytest
from uuid import uuid4

from app.modules.categories.application.category_service import CategoryService
from app.modules.categories.domain.enums import CategoryStatus
from app.modules.categories.domain.exceptions import DuplicateCategoryNameError
from app.modules.categories.infrastructure.repository import CategoryRepository


@pytest.mark.asyncio
async def test_category_service_create_and_duplicate(session) -> None:
    service = CategoryService(session)
    actor_id = uuid4()
    category = await service.create_category(
        actor_id=actor_id,
        name="Networking",
        description=None,
        icon="network",
    )
    assert category.name == "Networking"

    with pytest.raises(DuplicateCategoryNameError):
        await service.create_category(
            actor_id=actor_id,
            name="Networking",
            description=None,
            icon="network",
        )


@pytest.mark.asyncio
async def test_category_repository_list_active_only(session) -> None:
    repo = CategoryRepository(session)
    await repo.create(
        name="Active Cat",
        description=None,
        icon="a",
        display_order=1,
        status=CategoryStatus.ACTIVE,
    )
    await repo.create(
        name="Hidden Cat",
        description=None,
        icon="h",
        display_order=2,
        status=CategoryStatus.HIDDEN,
    )
    active, total = await repo.list_categories(page=1, page_size=20, status=CategoryStatus.ACTIVE)
    assert total == 1
    assert active[0].name == "Active Cat"
