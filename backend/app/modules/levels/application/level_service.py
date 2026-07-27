from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.application.category_service import CategoryService
from app.modules.categories.domain.exceptions import CategoryNotFoundError
from app.modules.levels.domain import events as level_events
from app.modules.levels.domain.entities import Level
from app.modules.levels.domain.enums import LevelStatus
from app.modules.levels.domain.exceptions import (
    InvalidLevelPrerequisiteError,
    LevelNotFoundError,
)
from app.modules.levels.domain.interfaces import LevelRepositoryProtocol
from app.modules.levels.infrastructure.repository import LevelRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class LevelService:
    def __init__(
        self,
        session: AsyncSession,
        repository: LevelRepositoryProtocol | None = None,
        category_service: CategoryService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or LevelRepository(session)
        self._categories = category_service or CategoryService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_level(
        self,
        *,
        actor_id: UUID,
        category_id: UUID,
        name: str,
        description: str | None,
        display_order: int | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Level:
        await self._ensure_category_exists(category_id, include_hidden=True)
        config = unlock_config or {}
        await self._validate_unlock_config(category_id, config)
        order = display_order if display_order is not None else await self._repo.get_max_display_order(category_id) + 1
        level = await self._repo.create(
            category_id=category_id,
            name=name,
            description=description,
            display_order=order,
            status=LevelStatus.ACTIVE,
            unlock_config=config,
        )
        await self._dispatcher.publish(
            level_events.level_created(level.id, level.category_id, level.name)
        )
        await self._audit.record(
            actor_id=actor_id,
            action="level.created",
            resource="level",
            metadata={"levelId": str(level.id), "categoryId": str(category_id)},
        )
        return level

    async def get_level(self, level_id: UUID, *, include_hidden: bool) -> Level:
        level = await self._repo.get_by_id(level_id)
        if level is None:
            raise LevelNotFoundError()
        if not include_hidden and level.status != LevelStatus.ACTIVE:
            raise LevelNotFoundError()
        return level

    async def list_levels(
        self,
        *,
        page: int,
        page_size: int,
        include_hidden: bool,
        category_id: UUID | None = None,
    ) -> tuple[list[Level], int]:
        status = None if include_hidden else LevelStatus.ACTIVE
        if category_id is not None:
            await self._ensure_category_exists(category_id, include_hidden=include_hidden)
            return await self._repo.list_by_category(
                category_id, page=page, page_size=page_size, status=status
            )
        return await self._repo.list_all(page=page, page_size=page_size, status=status)

    async def update_level(
        self,
        *,
        actor_id: UUID,
        level_id: UUID,
        name: str | None = None,
        description: str | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Level:
        existing = await self._repo.get_by_id(level_id)
        if existing is None:
            raise LevelNotFoundError()
        if unlock_config is not None:
            await self._validate_unlock_config(existing.category_id, unlock_config)
        updated = await self._repo.update(
            level_id,
            name=name,
            description=description,
            unlock_config=unlock_config,
        )
        if updated is None:
            raise LevelNotFoundError()
        await self._dispatcher.publish(
            level_events.level_updated(updated.id, updated.category_id)
        )
        await self._audit.record(
            actor_id=actor_id,
            action="level.updated",
            resource="level",
            metadata={"levelId": str(level_id)},
        )
        return updated

    async def hide_level(self, *, actor_id: UUID, level_id: UUID) -> Level:
        updated = await self._repo.update(level_id, status=LevelStatus.HIDDEN)
        if updated is None:
            raise LevelNotFoundError()
        await self._dispatcher.publish(level_events.level_hidden(level_id))
        await self._audit.record(
            actor_id=actor_id,
            action="level.hidden",
            resource="level",
            metadata={"levelId": str(level_id)},
        )
        return updated

    async def restore_level(self, *, actor_id: UUID, level_id: UUID) -> Level:
        updated = await self._repo.update(level_id, status=LevelStatus.ACTIVE)
        if updated is None:
            raise LevelNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="level.restored",
            resource="level",
            metadata={"levelId": str(level_id)},
        )
        return updated

    async def reorder_level(
        self,
        *,
        actor_id: UUID,
        level_id: UUID,
        display_order: int,
    ) -> Level:
        updated = await self._repo.update_display_order(level_id, display_order)
        if updated is None:
            raise LevelNotFoundError()
        await self._audit.record(
            actor_id=actor_id,
            action="level.reordered",
            resource="level",
            metadata={"levelId": str(level_id), "displayOrder": display_order},
        )
        return updated

    async def level_exists(self, level_id: UUID) -> bool:
        return await self._repo.get_by_id(level_id) is not None

    async def _ensure_category_exists(self, category_id: UUID, *, include_hidden: bool) -> None:
        try:
            await self._categories.get_category(category_id, include_hidden=include_hidden)
        except CategoryNotFoundError as exc:
            raise CategoryNotFoundError() from exc

    async def _validate_unlock_config(self, category_id: UUID, config: dict[str, Any]) -> None:
        prerequisite_id = config.get("prerequisiteLevelId")
        if prerequisite_id is None:
            return
        try:
            prerequisite_uuid = UUID(str(prerequisite_id))
        except ValueError as exc:
            raise InvalidLevelPrerequisiteError() from exc
        if not await self._repo.exists_in_category(prerequisite_uuid, category_id):
            raise InvalidLevelPrerequisiteError()
