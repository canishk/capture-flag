from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.submissions.domain.entities import Submission
from app.modules.submissions.domain.enums import SubmissionStatus
from app.modules.submissions.infrastructure.models import SubmissionModel


class SubmissionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        challenge_id: UUID,
        answer: str,
        attempt_number: int,
        evaluation_strategy_snapshot: dict[str, Any],
    ) -> Submission:
        model = SubmissionModel(
            user_id=user_id,
            challenge_id=challenge_id,
            answer=answer,
            attempt_number=attempt_number,
            status=SubmissionStatus.PENDING,
            evaluation_strategy_snapshot=evaluation_strategy_snapshot,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_id(self, submission_id: UUID) -> Submission | None:
        result = await self._session.execute(
            select(SubmissionModel).where(SubmissionModel.id == submission_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_next_attempt_number(self, user_id: UUID, challenge_id: UUID) -> int:
        result = await self._session.scalar(
            select(func.max(SubmissionModel.attempt_number)).where(
                SubmissionModel.user_id == user_id,
                SubmissionModel.challenge_id == challenge_id,
            )
        )
        return int(result or 0) + 1

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        page: int,
        page_size: int,
        challenge_id: UUID | None = None,
    ) -> tuple[list[Submission], int]:
        stmt = select(SubmissionModel).where(SubmissionModel.user_id == user_id)
        count_stmt = select(func.count()).select_from(SubmissionModel).where(
            SubmissionModel.user_id == user_id
        )
        if challenge_id is not None:
            stmt = stmt.where(SubmissionModel.challenge_id == challenge_id)
            count_stmt = count_stmt.where(SubmissionModel.challenge_id == challenge_id)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(SubmissionModel.created_at.desc())
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
        user_id: UUID | None = None,
        challenge_id: UUID | None = None,
        status: SubmissionStatus | None = None,
    ) -> tuple[list[Submission], int]:
        stmt = select(SubmissionModel)
        count_stmt = select(func.count()).select_from(SubmissionModel)
        if user_id is not None:
            stmt = stmt.where(SubmissionModel.user_id == user_id)
            count_stmt = count_stmt.where(SubmissionModel.user_id == user_id)
        if challenge_id is not None:
            stmt = stmt.where(SubmissionModel.challenge_id == challenge_id)
            count_stmt = count_stmt.where(SubmissionModel.challenge_id == challenge_id)
        if status is not None:
            stmt = stmt.where(SubmissionModel.status == status)
            count_stmt = count_stmt.where(SubmissionModel.status == status)
        total = int(await self._session.scalar(count_stmt) or 0)
        stmt = (
            stmt.order_by(SubmissionModel.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(m) for m in result.scalars().all()], total

    async def update_status(
        self,
        submission_id: UUID,
        *,
        status: SubmissionStatus,
        feedback: str | None = None,
        processing_time_ms: int | None = None,
    ) -> Submission | None:
        model = await self._get_model(submission_id)
        if model is None:
            return None
        model.status = status
        if feedback is not None:
            model.feedback = feedback
        if processing_time_ms is not None:
            model.processing_time_ms = processing_time_ms
        await self._session.flush()
        return self._to_entity(model)

    async def _get_model(self, submission_id: UUID) -> SubmissionModel | None:
        result = await self._session.execute(
            select(SubmissionModel).where(SubmissionModel.id == submission_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def _to_entity(model: SubmissionModel) -> Submission:
        return Submission(
            id=model.id,
            user_id=model.user_id,
            challenge_id=model.challenge_id,
            answer=model.answer,
            attempt_number=model.attempt_number,
            status=model.status,
            evaluation_strategy_snapshot=model.evaluation_strategy_snapshot,
            feedback=model.feedback,
            processing_time_ms=model.processing_time_ms,
            submitted_at=model.created_at,
            updated_at=model.updated_at,
        )
