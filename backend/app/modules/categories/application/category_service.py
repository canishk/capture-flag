from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.domain import events as category_events
from app.modules.categories.domain.entities import Category
from app.modules.categories.domain.enums import CategoryStatus
from app.modules.categories.domain.exceptions import (
    CategoryNotFoundError,
    DuplicateCategoryNameError,
)
from app.modules.categories.domain.interfaces import CategoryRepositoryProtocol
from app.modules.categories.infrastructure.repository import CategoryRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class CategoryService:
    def __init__(
        self,
        session: AsyncSession,
        repository: CategoryRepositoryProtocol | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or CategoryRepository(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_category(
        self,
        *,
        actor_id: UUID,
        name: str,
        description: str | None,
        icon: str,
        display_order: int | None = None,
    ) -> Category:
        if await self._repo.get_by_name(name) is not None:
            raise DuplicateCategoryNameError()
        order = display_order if display_order is not None else await self._repo.get_max_display_order() + 1
        category = await self._repo.create(
            name=name,
            description=description,
            icon=icon,
            display_order=order,
            status=CategoryStatus.ACTIVE,
        )
        await self._dispatcher.publish(category_events.category_created(category.id, category.name))
        await self._audit.record(
            actor_id=actor_id,
            action="category.created",
            resource="category",
            metadata={"categoryId": str(category.id)},
        )
        return category

    async def get_category(self, category_id: UUID, *, include_hidden: bool) -> Category:
        category = await self._repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError()
        if not include_hidden and category.status != CategoryStatus.ACTIVE:
            raise CategoryNotFoundError()
        return category

    async def list_categories(
        self,
        *,
        page: int,
        page_size: int,
        include_hidden: bool,
        search: str | None = None,
    ) -> tuple[list[Category], int]:
        status = None if include_hidden else CategoryStatus.ACTIVE
        return await self._repo.list_categories(
            page=page,
            page_size=page_size,
            status=status,
            search=search,
        )

    async def update_category(
        self,
        *,
        actor_id: UUID,
        category_id: UUID,
        name: str | None = None,
        description: str | None = None,
        icon: str | None = None,
    ) -> Category:
        existing = await self._repo.get_by_id(category_id)
        if existing is None:
            raise CategoryNotFoundError()
        if name is not None and name != existing.name:
            duplicate = await self._repo.get_by_name(name)
            if duplicate is not None:
                raise DuplicateCategoryNameError()
        updated = await self._repo.update(
            category_id,
            name=name,
            description=description,
            icon=icon,
        )
        if updated is None:
            raise CategoryNotFoundError()
        await self._dispatcher.publish(category_events.category_updated(updated.id, updated.name))
        await self._audit.record(
            actor_id=actor_id,
            action="category.updated",
            resource="category",
            metadata={"categoryId": str(category_id)},
        )
        return updated

    async def hide_category(self, *, actor_id: UUID, category_id: UUID) -> Category:
        updated = await self._repo.update(category_id, status=CategoryStatus.HIDDEN)
        if updated is None:
            raise CategoryNotFoundError()
        await self._dispatcher.publish(category_events.category_hidden(category_id))
        await self._audit.record(
            actor_id=actor_id,
            action="category.hidden",
            resource="category",
            metadata={"categoryId": str(category_id)},
        )
        return updated

    async def restore_category(self, *, actor_id: UUID, category_id: UUID) -> Category:
        updated = await self._repo.update(category_id, status=CategoryStatus.ACTIVE)
        if updated is None:
            raise CategoryNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="category.restored",
            resource="category",
            metadata={"categoryId": str(category_id)},
        )
        return updated

    async def reorder_category(
        self,
        *,
        actor_id: UUID,
        category_id: UUID,
        display_order: int,
    ) -> Category:
        updated = await self._repo.update_display_order(category_id, display_order)
        if updated is None:
            raise CategoryNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="category.reordered",
            resource="category",
            metadata={"categoryId": str(category_id), "displayOrder": display_order},
        )
        return updated

    async def category_exists(self, category_id: UUID) -> bool:
        return await self._repo.get_by_id(category_id) is not None
