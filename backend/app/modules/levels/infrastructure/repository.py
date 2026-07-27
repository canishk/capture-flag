from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.levels.domain.entities import Level
from app.modules.levels.domain.enums import LevelStatus
from app.modules.levels.infrastructure.models import LevelModel


class LevelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        category_id: UUID,
        name: str,
        description: str | None,
        display_order: int,
        status: LevelStatus,
        unlock_config: dict[str, Any],
    ) -> Level:
        model = LevelModel(
            category_id=category_id,
            name=name,
            description=description,
            display_order=display_order,
            status=status,
            unlock_config=unlock_config,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, level_id: UUID) -> Level | None:
        result = await self._session.execute(select(LevelModel).where(LevelModel.id == level_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_category(
        self,
        category_id: UUID,
        *,
        page: int,
        page_size: int,
        status: LevelStatus | None = None,
    ) -> tuple[list[Level], int]:
        stmt = select(LevelModel).where(LevelModel.category_id == category_id)
        count_stmt = select(func.count()).select_from(LevelModel).where(
            LevelModel.category_id == category_id
        )
        if status is not None:
            stmt = stmt.where(LevelModel.status == status)
            count_stmt = count_stmt.where(LevelModel.status == status)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(LevelModel.display_order.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def list_all(
        self,
        *,
        page: int,
        page_size: int,
        status: LevelStatus | None = None,
    ) -> tuple[list[Level], int]:
        stmt = select(LevelModel)
        count_stmt = select(func.count()).select_from(LevelModel)
        if status is not None:
            stmt = stmt.where(LevelModel.status == status)
            count_stmt = count_stmt.where(LevelModel.status == status)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(LevelModel.category_id, LevelModel.display_order.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update(
        self,
        level_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        status: LevelStatus | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Level | None:
        model = await self._get_model(level_id)
        if model is None:
            return None
        if name is not None:
            model.name = name
        if description is not None:
            model.description = description
        if status is not None:
            model.status = status
        if unlock_config is not None:
            model.unlock_config = unlock_config
        await self._session.flush()
        return self._to_entity(model)

    async def update_display_order(self, level_id: UUID, display_order: int) -> Level | None:
        model = await self._get_model(level_id)
        if model is None:
            return None
        model.display_order = display_order
        await self._session.flush()
        return self._to_entity(model)

    async def get_max_display_order(self, category_id: UUID) -> int:
        result = await self._session.scalar(
            select(func.max(LevelModel.display_order)).where(LevelModel.category_id == category_id)
        )
        return int(result or 0)

    async def exists_in_category(self, level_id: UUID, category_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(LevelModel)
            .where(LevelModel.id == level_id, LevelModel.category_id == category_id)
        )
        return int(result or 0) > 0

    async def _get_model(self, level_id: UUID) -> LevelModel | None:
        result = await self._session.execute(select(LevelModel).where(LevelModel.id == level_id))
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: LevelModel) -> Level:
        return Level(
            id=model.id,
            category_id=model.category_id,
            name=model.name,
            description=model.description,
            display_order=model.display_order,
            status=model.status,
            unlock_config=model.unlock_config,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
