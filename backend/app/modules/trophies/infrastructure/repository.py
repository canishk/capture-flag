from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.trophies.domain.entities import TrophyAward, TrophyDefinition
from app.modules.trophies.domain.enums import TrophyTriggerType
from app.modules.trophies.infrastructure.models import TrophyAwardModel, TrophyDefinitionModel


class TrophyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_definition(
        self,
        *,
        code: str,
        name: str,
        description: str,
        icon: str,
        trigger_type: TrophyTriggerType,
        criteria: dict[str, Any],
        is_repeatable: bool,
    ) -> TrophyDefinition:
        model = TrophyDefinitionModel(
            code=code,
            name=name,
            description=description,
            icon=icon,
            trigger_type=trigger_type,
            criteria=criteria,
            is_repeatable=is_repeatable,
            is_active=True,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_definition(model)

    async def get_definition_by_id(self, trophy_id: UUID) -> TrophyDefinition | None:
        result = await self._session.execute(
            select(TrophyDefinitionModel).where(TrophyDefinitionModel.id == trophy_id)
        )
        model = result.scalar_one_or_none()
        return self._to_definition(model) if model else None

    async def get_definition_by_code(self, code: str) -> TrophyDefinition | None:
        result = await self._session.execute(
            select(TrophyDefinitionModel).where(TrophyDefinitionModel.code == code)
        )
        model = result.scalar_one_or_none()
        return self._to_definition(model) if model else None

    async def list_definitions(
        self, *, page: int, page_size: int, active_only: bool
    ) -> tuple[list[TrophyDefinition], int]:
        stmt = select(TrophyDefinitionModel)
        count_stmt = select(func.count()).select_from(TrophyDefinitionModel)
        if active_only:
            stmt = stmt.where(TrophyDefinitionModel.is_active.is_(True))
            count_stmt = count_stmt.where(TrophyDefinitionModel.is_active.is_(True))
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(TrophyDefinitionModel.name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_definition(m) for m in result.scalars().all()], total

    async def list_by_trigger(self, trigger_type: TrophyTriggerType) -> list[TrophyDefinition]:
        result = await self._session.execute(
            select(TrophyDefinitionModel).where(
                TrophyDefinitionModel.trigger_type == trigger_type,
                TrophyDefinitionModel.is_active.is_(True),
            )
        )
        return [self._to_definition(m) for m in result.scalars().all()]

    async def has_award(self, trophy_id: UUID, user_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(TrophyAwardModel)
            .where(TrophyAwardModel.trophy_id == trophy_id, TrophyAwardModel.user_id == user_id)
        )
        return int(result or 0) > 0

    async def count_user_awards(self, user_id: UUID) -> int:
        return int(
            await self._session.scalar(
                select(func.count())
                .select_from(TrophyAwardModel)
                .where(TrophyAwardModel.user_id == user_id)
            )
            or 0
        )

    async def create_award(
        self, *, trophy_id: UUID, user_id: UUID, source_event_id: UUID
    ) -> TrophyAward:
        model = TrophyAwardModel(
            trophy_id=trophy_id,
            user_id=user_id,
            source_event_id=source_event_id,
            awarded_at=datetime.now(UTC),
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_award(model)

    async def list_user_awards(
        self, user_id: UUID, *, page: int, page_size: int
    ) -> tuple[list[tuple[TrophyAward, TrophyDefinition]], int]:
        stmt = (
            select(TrophyAwardModel, TrophyDefinitionModel)
            .join(TrophyDefinitionModel, TrophyDefinitionModel.id == TrophyAwardModel.trophy_id)
            .where(TrophyAwardModel.user_id == user_id)
        )
        count_stmt = (
            select(func.count())
            .select_from(TrophyAwardModel)
            .where(TrophyAwardModel.user_id == user_id)
        )
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(TrophyAwardModel.awarded_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        rows = [(self._to_award(a), self._to_definition(d)) for a, d in result.all()]
        return rows, total

    @staticmethod
    def _to_definition(model: TrophyDefinitionModel) -> TrophyDefinition:
        return TrophyDefinition(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            icon=model.icon,
            trigger_type=model.trigger_type,
            criteria=model.criteria,
            is_repeatable=model.is_repeatable,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_award(model: TrophyAwardModel) -> TrophyAward:
        return TrophyAward(
            id=model.id,
            trophy_id=model.trophy_id,
            user_id=model.user_id,
            source_event_id=model.source_event_id,
            awarded_at=model.awarded_at,
        )
