from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.progress.domain.entities import LearnerProgress, ProgressSummary
from app.modules.progress.infrastructure.models import (
    CategoryCompletionModel,
    ChallengeCompletionModel,
    LearnerProgressModel,
    LevelCompletionModel,
)


class ProgressRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create_progress(self, user_id: UUID) -> LearnerProgress:
        model = await self._get_progress_model(user_id)
        if model is None:
            model = LearnerProgressModel(
                user_id=user_id,
                total_xp=0,
                challenges_attempted=0,
                challenges_completed=0,
            )
            self._session.add(model)
            await self._session.flush()
        return self._to_progress(model)

    async def increment_attempt(self, user_id: UUID, challenge_id: UUID) -> LearnerProgress:
        model = await self._get_progress_model(user_id)
        if model is None:
            model = LearnerProgressModel(
                user_id=user_id,
                total_xp=0,
                challenges_attempted=0,
                challenges_completed=0,
            )
            self._session.add(model)
        model.challenges_attempted += 1
        model.last_active_challenge_id = challenge_id
        await self._session.flush()
        return self._to_progress(model)

    async def has_challenge_completion(self, user_id: UUID, challenge_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(ChallengeCompletionModel)
            .where(
                ChallengeCompletionModel.user_id == user_id,
                ChallengeCompletionModel.challenge_id == challenge_id,
            )
        )
        return int(result or 0) > 0

    async def record_challenge_completion(
        self,
        *,
        user_id: UUID,
        challenge_id: UUID,
        level_id: UUID,
        category_id: UUID,
        score: int,
    ) -> None:
        if await self.has_challenge_completion(user_id, challenge_id):
            return
        self._session.add(
            ChallengeCompletionModel(
                user_id=user_id,
                challenge_id=challenge_id,
                level_id=level_id,
                category_id=category_id,
                score=score,
                completed_at=datetime.now(UTC),
            )
        )
        model = await self._get_progress_model(user_id)
        if model is None:
            model = LearnerProgressModel(
                user_id=user_id,
                total_xp=0,
                challenges_attempted=0,
                challenges_completed=0,
            )
            self._session.add(model)
        model.total_xp += score
        model.challenges_completed += 1
        model.last_active_challenge_id = challenge_id
        await self._session.flush()

    async def has_level_completion(self, user_id: UUID, level_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(LevelCompletionModel)
            .where(
                LevelCompletionModel.user_id == user_id,
                LevelCompletionModel.level_id == level_id,
            )
        )
        return int(result or 0) > 0

    async def record_level_completion(self, user_id: UUID, level_id: UUID, category_id: UUID) -> None:
        if await self.has_level_completion(user_id, level_id):
            return
        self._session.add(
            LevelCompletionModel(
                user_id=user_id,
                level_id=level_id,
                category_id=category_id,
                completed_at=datetime.now(UTC),
            )
        )
        await self._session.flush()

    async def has_category_completion(self, user_id: UUID, category_id: UUID) -> bool:
        result = await self._session.scalar(
            select(func.count())
            .select_from(CategoryCompletionModel)
            .where(
                CategoryCompletionModel.user_id == user_id,
                CategoryCompletionModel.category_id == category_id,
            )
        )
        return int(result or 0) > 0

    async def record_category_completion(self, user_id: UUID, category_id: UUID) -> None:
        if await self.has_category_completion(user_id, category_id):
            return
        self._session.add(
            CategoryCompletionModel(
                user_id=user_id,
                category_id=category_id,
                completed_at=datetime.now(UTC),
            )
        )
        await self._session.flush()

    async def get_completed_challenge_ids_for_level(self, user_id: UUID, level_id: UUID) -> set[UUID]:
        result = await self._session.execute(
            select(ChallengeCompletionModel.challenge_id).where(
                ChallengeCompletionModel.user_id == user_id,
                ChallengeCompletionModel.level_id == level_id,
            )
        )
        return {row[0] for row in result.all()}

    async def get_completed_level_ids_for_category(
        self, user_id: UUID, category_id: UUID
    ) -> set[UUID]:
        result = await self._session.execute(
            select(LevelCompletionModel.level_id).where(
                LevelCompletionModel.user_id == user_id,
                LevelCompletionModel.category_id == category_id,
            )
        )
        return {row[0] for row in result.all()}

    async def get_summary(self, user_id: UUID, total_published_challenges: int) -> ProgressSummary:
        progress = await self.get_or_create_progress(user_id)
        levels_completed = int(
            await self._session.scalar(
                select(func.count())
                .select_from(LevelCompletionModel)
                .where(LevelCompletionModel.user_id == user_id)
            )
            or 0
        )
        categories_completed = int(
            await self._session.scalar(
                select(func.count())
                .select_from(CategoryCompletionModel)
                .where(CategoryCompletionModel.user_id == user_id)
            )
            or 0
        )
        completion_pct = (
            (progress.challenges_completed / total_published_challenges) * 100
            if total_published_challenges > 0
            else 0.0
        )
        return ProgressSummary(
            user_id=user_id,
            total_xp=progress.total_xp,
            challenges_attempted=progress.challenges_attempted,
            challenges_completed=progress.challenges_completed,
            levels_completed=levels_completed,
            categories_completed=categories_completed,
            completion_percentage=round(completion_pct, 2),
            last_active_challenge_id=progress.last_active_challenge_id,
        )

    async def _get_progress_model(self, user_id: UUID) -> LearnerProgressModel | None:
        result = await self._session.execute(
            select(LearnerProgressModel).where(LearnerProgressModel.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_progress(model: LearnerProgressModel) -> LearnerProgress:
        return LearnerProgress(
            user_id=model.user_id,
            total_xp=model.total_xp,
            challenges_attempted=model.challenges_attempted,
            challenges_completed=model.challenges_completed,
            last_active_challenge_id=model.last_active_challenge_id,
            updated_at=model.updated_at,
        )
