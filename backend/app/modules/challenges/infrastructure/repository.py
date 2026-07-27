from typing import Any
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.domain.entities import Challenge
from app.modules.challenges.domain.enums import (
    ChallengeDifficulty,
    ChallengeStatus,
    ChallengeType,
)
from app.modules.challenges.infrastructure.models import ChallengeModel


class ChallengeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        category_id: UUID,
        level_id: UUID,
        title: str,
        summary: str | None,
        description: str,
        objectives: list[str],
        challenge_type: ChallengeType,
        difficulty: ChallengeDifficulty,
        estimated_duration_minutes: int | None,
        status: ChallengeStatus,
        display_order: int,
        base_score: int,
        scoring_config: dict[str, Any],
        evaluation_strategy: dict[str, Any],
        unlock_config: dict[str, Any],
        is_required: bool,
    ) -> Challenge:
        model = ChallengeModel(
            category_id=category_id,
            level_id=level_id,
            title=title,
            summary=summary,
            description=description,
            objectives=objectives,
            challenge_type=challenge_type,
            difficulty=difficulty,
            estimated_duration_minutes=estimated_duration_minutes,
            status=status,
            display_order=display_order,
            base_score=base_score,
            scoring_config=scoring_config,
            evaluation_strategy=evaluation_strategy,
            unlock_config=unlock_config,
            is_required=is_required,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, challenge_id: UUID) -> Challenge | None:
        result = await self._session.execute(
            select(ChallengeModel).where(ChallengeModel.id == challenge_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_title_in_level(self, level_id: UUID, title: str) -> Challenge | None:
        result = await self._session.execute(
            select(ChallengeModel).where(
                ChallengeModel.level_id == level_id,
                ChallengeModel.title == title,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_challenges(
        self,
        *,
        page: int,
        page_size: int,
        status: ChallengeStatus | None = None,
        category_id: UUID | None = None,
        level_id: UUID | None = None,
        search: str | None = None,
    ) -> tuple[list[Challenge], int]:
        stmt = select(ChallengeModel)
        count_stmt = select(func.count()).select_from(ChallengeModel)
        if status is not None:
            stmt = stmt.where(ChallengeModel.status == status)
            count_stmt = count_stmt.where(ChallengeModel.status == status)
        if category_id is not None:
            stmt = stmt.where(ChallengeModel.category_id == category_id)
            count_stmt = count_stmt.where(ChallengeModel.category_id == category_id)
        if level_id is not None:
            stmt = stmt.where(ChallengeModel.level_id == level_id)
            count_stmt = count_stmt.where(ChallengeModel.level_id == level_id)
        if search:
            pattern = f"%{search}%"
            condition = or_(
                ChallengeModel.title.ilike(pattern),
                ChallengeModel.summary.ilike(pattern),
            )
            stmt = stmt.where(condition)
            count_stmt = count_stmt.where(condition)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(ChallengeModel.level_id, ChallengeModel.display_order.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update(self, challenge_id: UUID, **kwargs: Any) -> Challenge | None:
        model = await self._get_model(challenge_id)
        if model is None:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)
        await self._session.flush()
        return self._to_entity(model)

    async def update_display_order(self, challenge_id: UUID, display_order: int) -> Challenge | None:
        model = await self._get_model(challenge_id)
        if model is None:
            return None
        model.display_order = display_order
        await self._session.flush()
        return self._to_entity(model)

    async def get_max_display_order(self, level_id: UUID) -> int:
        result = await self._session.scalar(
            select(func.max(ChallengeModel.display_order)).where(
                ChallengeModel.level_id == level_id
            )
        )
        return int(result or 0)

    async def _get_model(self, challenge_id: UUID) -> ChallengeModel | None:
        result = await self._session.execute(
            select(ChallengeModel).where(ChallengeModel.id == challenge_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: ChallengeModel) -> Challenge:
        return Challenge(
            id=model.id,
            category_id=model.category_id,
            level_id=model.level_id,
            title=model.title,
            summary=model.summary,
            description=model.description,
            objectives=model.objectives,
            challenge_type=model.challenge_type,
            difficulty=model.difficulty,
            estimated_duration_minutes=model.estimated_duration_minutes,
            status=model.status,
            display_order=model.display_order,
            base_score=model.base_score,
            scoring_config=model.scoring_config,
            evaluation_strategy=model.evaluation_strategy,
            unlock_config=model.unlock_config,
            is_required=model.is_required,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
