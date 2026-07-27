import time
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.exceptions import ChallengeNotFoundError
from app.modules.evaluations.domain import events as evaluation_events
from app.modules.evaluations.domain.enums import EvaluationStatus, EvaluationStrategyType
from app.modules.evaluations.domain.exceptions import (
    EvaluationConfigurationError,
    EvaluationNotFoundError,
    UnsupportedEvaluationStrategyError,
)
from app.modules.evaluations.domain.interfaces import EvaluationRepositoryProtocol
from app.modules.evaluations.domain.strategies import EvaluationStrategyRegistry
from app.modules.evaluations.infrastructure.repository import EvaluationRepository
from app.modules.submissions.application.submission_service import SubmissionService
from app.modules.submissions.domain.enums import SubmissionStatus
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class EvaluationService:
    def __init__(
        self,
        session: AsyncSession,
        repository: EvaluationRepositoryProtocol | None = None,
        submission_service: SubmissionService | None = None,
        challenge_service: ChallengeService | None = None,
        dispatcher: EventDispatcher | None = None,
        strategy_registry: EvaluationStrategyRegistry | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or EvaluationRepository(session)
        self._submissions = submission_service or SubmissionService(session)
        self._challenges = challenge_service or ChallengeService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()
        self._strategies = strategy_registry or EvaluationStrategyRegistry()

    async def evaluate_submission(self, submission_id: UUID) -> None:
        if await self._repo.get_by_submission_id(submission_id) is not None:
            return
        submission = await self._submissions.get_submission_for_evaluation(submission_id)
        await self._submissions.update_submission_status(
            submission_id=submission_id,
            status=SubmissionStatus.EVALUATING,
        )
        start = time.perf_counter()
        strategy_config: dict = {}
        try:
            challenge = await self._challenges.get_challenge(
                submission.challenge_id, include_non_published=True
            )
            strategy_config = challenge.evaluation_strategy
            strategy_type = EvaluationStrategyType(strategy_config.get("type", "exact_match"))
            result = self._strategies.evaluate(
                strategy_type, submission.answer, strategy_config, challenge.base_score
            )
            processing_ms = int((time.perf_counter() - start) * 1000)
            evaluation = await self._repo.create(
                submission_id=submission_id,
                user_id=submission.user_id,
                challenge_id=submission.challenge_id,
                strategy_type=strategy_type.value,
                passed=result.passed,
                score=result.score,
                feedback=result.feedback,
                status=EvaluationStatus.COMPLETED.value,
                processing_time_ms=processing_ms,
                metadata=result.metadata or {},
            )
            await self._submissions.update_submission_status(
                submission_id=submission_id,
                status=SubmissionStatus.PASSED if result.passed else SubmissionStatus.FAILED,
                feedback=result.feedback,
                processing_time_ms=processing_ms,
            )
            await self._dispatcher.publish(
                evaluation_events.evaluation_completed(
                    evaluation.id,
                    submission_id,
                    submission.user_id,
                    submission.challenge_id,
                    result.passed,
                    result.score,
                )
            )
            await self._audit.record(
                actor_id=submission.user_id,
                action="evaluation.completed",
                resource="evaluation",
                metadata={"evaluationId": str(evaluation.id), "passed": result.passed},
            )
        except (UnsupportedEvaluationStrategyError, EvaluationConfigurationError, ChallengeNotFoundError) as exc:
            processing_ms = int((time.perf_counter() - start) * 1000)
            evaluation = await self._repo.create(
                submission_id=submission_id,
                user_id=submission.user_id,
                challenge_id=submission.challenge_id,
                strategy_type=strategy_config.get("type", "unknown"),
                passed=False,
                score=0,
                feedback="Evaluation could not be completed.",
                status=EvaluationStatus.ERROR.value,
                processing_time_ms=processing_ms,
                metadata={"error": str(exc)},
            )
            await self._submissions.update_submission_status(
                submission_id=submission_id,
                status=SubmissionStatus.ERROR,
                feedback="Evaluation could not be completed.",
                processing_time_ms=processing_ms,
            )
            await self._dispatcher.publish(
                evaluation_events.evaluation_failed(
                    evaluation.id,
                    submission_id,
                    submission.user_id,
                    submission.challenge_id,
                    str(exc),
                )
            )

    async def get_evaluation_by_submission(self, submission_id: UUID):
        evaluation = await self._repo.get_by_submission_id(submission_id)
        if evaluation is None:
            raise EvaluationNotFoundError()
        return evaluation

    async def preview_evaluation(self, answer: str, evaluation_strategy: dict, base_score: int):
        strategy_type = EvaluationStrategyType(evaluation_strategy.get("type", "exact_match"))
        return self._strategies.evaluate(strategy_type, answer, evaluation_strategy, base_score)

    def list_strategies(self) -> list[str]:
        return [s.value for s in EvaluationStrategyType]
