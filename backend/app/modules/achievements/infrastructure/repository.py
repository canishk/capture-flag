from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.achievements.domain.entities import AchievementDefinition, UserAchievementProgress
from app.modules.achievements.domain.enums import AchievementCriteriaType
from app.modules.achievements.infrastructure.models import (
    AchievementDefinitionModel,
    UserAchievementProgressModel,
)


class AchievementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_definition(
        self,
        *,
        code: str,
        name: str,
        description: str,
        icon: str,
        criteria_type: AchievementCriteriaType,
        target_count: int,
        is_hidden: bool,
    ) -> AchievementDefinition:
        model = AchievementDefinitionModel(
            code=code,
            name=name,
            description=description,
            icon=icon,
            criteria_type=criteria_type,
            target_count=target_count,
            is_hidden=is_hidden,
            is_active=True,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_definition(model)

    async def get_by_id(self, achievement_id: UUID) -> AchievementDefinition | None:
        result = await self._session.execute(
            select(AchievementDefinitionModel).where(AchievementDefinitionModel.id == achievement_id)
        )
        model = result.scalar_one_or_none()
        return self._to_definition(model) if model else None

    async def get_by_code(self, code: str) -> AchievementDefinition | None:
        result = await self._session.execute(
            select(AchievementDefinitionModel).where(AchievementDefinitionModel.code == code)
        )
        model = result.scalar_one_or_none()
        return self._to_definition(model) if model else None

    async def list_definitions(
        self, *, page: int, page_size: int, include_hidden: bool
    ) -> tuple[list[AchievementDefinition], int]:
        stmt = select(AchievementDefinitionModel).where(AchievementDefinitionModel.is_active.is_(True))
        count_stmt = select(func.count()).select_from(AchievementDefinitionModel).where(
            AchievementDefinitionModel.is_active.is_(True)
        )
        if not include_hidden:
            stmt = stmt.where(AchievementDefinitionModel.is_hidden.is_(False))
            count_stmt = count_stmt.where(AchievementDefinitionModel.is_hidden.is_(False))
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(AchievementDefinitionModel.name.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_definition(m) for m in result.scalars().all()], total

    async def list_by_criteria(self, criteria_type: AchievementCriteriaType) -> list[AchievementDefinition]:
        result = await self._session.execute(
            select(AchievementDefinitionModel).where(
                AchievementDefinitionModel.criteria_type == criteria_type,
                AchievementDefinitionModel.is_active.is_(True),
            )
        )
        return [self._to_definition(m) for m in result.scalars().all()]

    async def get_progress(
        self, user_id: UUID, achievement_id: UUID
    ) -> UserAchievementProgress | None:
        result = await self._session.execute(
            select(UserAchievementProgressModel).where(
                UserAchievementProgressModel.user_id == user_id,
                UserAchievementProgressModel.achievement_id == achievement_id,
            )
        )
        model = result.scalar_one_or_none()
        return self._to_progress(model) if model else None

    async def upsert_progress(
        self, user_id: UUID, achievement_id: UUID, progress: int, unlocked: bool
    ) -> UserAchievementProgress:
        model = await self._session.scalar(
            select(UserAchievementProgressModel).where(
                UserAchievementProgressModel.user_id == user_id,
                UserAchievementProgressModel.achievement_id == achievement_id,
            )
        )
        if model is None:
            model = UserAchievementProgressModel(
                user_id=user_id,
                achievement_id=achievement_id,
                current_progress=progress,
                unlocked_at=datetime.now(UTC) if unlocked else None,
            )
            self._session.add(model)
        else:
            model.current_progress = progress
            if unlocked and model.unlocked_at is None:
                model.unlocked_at = datetime.now(UTC)
        await self._session.flush()
        return self._to_progress(model)

    async def list_user_progress(
        self, user_id: UUID, *, page: int, page_size: int
    ) -> tuple[list[tuple[UserAchievementProgress, AchievementDefinition]], int]:
        stmt = (
            select(UserAchievementProgressModel, AchievementDefinitionModel)
            .join(
                AchievementDefinitionModel,
                AchievementDefinitionModel.id == UserAchievementProgressModel.achievement_id,
            )
            .where(UserAchievementProgressModel.user_id == user_id)
        )
        count_stmt = (
            select(func.count())
            .select_from(UserAchievementProgressModel)
            .where(UserAchievementProgressModel.user_id == user_id)
        )
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = stmt.offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(stmt)
        return [(self._to_progress(p), self._to_definition(d)) for p, d in result.all()], total

    @staticmethod
    def _to_definition(model: AchievementDefinitionModel) -> AchievementDefinition:
        return AchievementDefinition(
            id=model.id,
            code=model.code,
            name=model.name,
            description=model.description,
            icon=model.icon,
            criteria_type=model.criteria_type,
            target_count=model.target_count,
            is_hidden=model.is_hidden,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def _to_progress(model: UserAchievementProgressModel) -> UserAchievementProgress:
        return UserAchievementProgress(
            user_id=model.user_id,
            achievement_id=model.achievement_id,
            current_progress=model.current_progress,
            unlocked_at=model.unlocked_at,
        )
