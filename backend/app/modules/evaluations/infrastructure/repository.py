from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.evaluations.domain.entities import Evaluation
from app.modules.evaluations.domain.enums import EvaluationStatus, EvaluationStrategyType
from app.modules.evaluations.infrastructure.models import EvaluationModel


class EvaluationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        submission_id: UUID,
        user_id: UUID,
        challenge_id: UUID,
        strategy_type: str,
        passed: bool,
        score: int,
        feedback: str,
        status: str,
        processing_time_ms: int,
        metadata: dict[str, Any],
    ) -> Evaluation:
        model = EvaluationModel(
            submission_id=submission_id,
            user_id=user_id,
            challenge_id=challenge_id,
            strategy_type=EvaluationStrategyType(strategy_type),
            passed=passed,
            score=score,
            feedback=feedback,
            status=EvaluationStatus(status),
            processing_time_ms=processing_time_ms,
            metadata_json=metadata,
        )
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_by_submission_id(self, submission_id: UUID) -> Evaluation | None:
        result = await self._session.execute(
            select(EvaluationModel).where(EvaluationModel.submission_id == submission_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_id(self, evaluation_id: UUID) -> Evaluation | None:
        result = await self._session.execute(
            select(EvaluationModel).where(EvaluationModel.id == evaluation_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: EvaluationModel) -> Evaluation:
        return Evaluation(
            id=model.id,
            submission_id=model.submission_id,
            user_id=model.user_id,
            challenge_id=model.challenge_id,
            strategy_type=model.strategy_type,
            passed=model.passed,
            score=model.score,
            feedback=model.feedback,
            status=model.status,
            processing_time_ms=model.processing_time_ms,
            metadata=model.metadata_json,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
