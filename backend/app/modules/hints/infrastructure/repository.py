from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.hints.domain.entities import Hint
from app.modules.hints.domain.enums import HintStatus
from app.modules.hints.infrastructure.models import HintModel


class HintRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        challenge_id: UUID,
        title: str,
        content: str,
        display_order: int,
        penalty_config: dict[str, Any],
        unlock_config: dict[str, Any],
        status: HintStatus,
    ) -> Hint:
        model = HintModel(
            challenge_id=challenge_id,
            title=title,
            content=content,
            display_order=display_order,
            penalty_config=penalty_config,
            unlock_config=unlock_config,
            status=status,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, hint_id: UUID) -> Hint | None:
        result = await self._session.execute(select(HintModel).where(HintModel.id == hint_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        status: HintStatus | None = None,
    ) -> tuple[list[Hint], int]:
        stmt = select(HintModel).where(HintModel.challenge_id == challenge_id)
        count_stmt = select(func.count()).select_from(HintModel).where(
            HintModel.challenge_id == challenge_id
        )
        if status is not None:
            stmt = stmt.where(HintModel.status == status)
            count_stmt = count_stmt.where(HintModel.status == status)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(HintModel.display_order.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update(self, hint_id: UUID, **kwargs: Any) -> Hint | None:
        model = await self._get_model(hint_id)
        if model is None:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)
        await self._session.flush()
        return self._to_entity(model)

    async def update_display_order(self, hint_id: UUID, display_order: int) -> Hint | None:
        model = await self._get_model(hint_id)
        if model is None:
            return None
        model.display_order = display_order
        await self._session.flush()
        return self._to_entity(model)

    async def get_max_display_order(self, challenge_id: UUID) -> int:
        result = await self._session.scalar(
            select(func.max(HintModel.display_order)).where(
                HintModel.challenge_id == challenge_id
            )
        )
        return int(result or 0)

    async def order_exists(
        self, challenge_id: UUID, display_order: int, exclude_id: UUID | None = None
    ) -> bool:
        stmt = select(func.count()).select_from(HintModel).where(
            HintModel.challenge_id == challenge_id,
            HintModel.display_order == display_order,
        )
        if exclude_id is not None:
            stmt = stmt.where(HintModel.id != exclude_id)
        return int(await self._session.scalar(stmt) or 0) > 0

    async def _get_model(self, hint_id: UUID) -> HintModel | None:
        result = await self._session.execute(select(HintModel).where(HintModel.id == hint_id))
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: HintModel) -> Hint:
        return Hint(
            id=model.id,
            challenge_id=model.challenge_id,
            title=model.title,
            content=model.content,
            display_order=model.display_order,
            penalty_config=model.penalty_config,
            unlock_config=model.unlock_config,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
