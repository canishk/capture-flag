from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.challenges.application.challenge_service import ChallengeService
from app.modules.challenges.domain.enums import ChallengeStatus
from app.modules.challenges.domain.exceptions import ChallengeNotFoundError
from app.modules.submissions.domain import events as submission_events
from app.modules.submissions.domain.entities import Submission
from app.modules.submissions.domain.enums import SubmissionStatus
from app.modules.submissions.domain.exceptions import (
    InvalidSubmissionError,
    SubmissionAccessDeniedError,
    SubmissionNotFoundError,
)
from app.modules.submissions.domain.interfaces import SubmissionRepositoryProtocol
from app.modules.submissions.infrastructure.repository import SubmissionRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class SubmissionService:
    def __init__(
        self,
        session: AsyncSession,
        repository: SubmissionRepositoryProtocol | None = None,
        challenge_service: ChallengeService | None = None,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = repository or SubmissionRepository(session)
        self._challenges = challenge_service or ChallengeService(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def create_submission(
        self,
        *,
        user_id: UUID,
        challenge_id: UUID,
        answer: str,
    ) -> Submission:
        if not answer.strip():
            raise InvalidSubmissionError("Answer is required")
        try:
            challenge = await self._challenges.get_challenge(
                challenge_id, include_non_published=False
            )
        except ChallengeNotFoundError as exc:
            raise InvalidSubmissionError("Challenge is not available") from exc
        if challenge.status == ChallengeStatus.ARCHIVED:
            raise InvalidSubmissionError("Challenge is archived")
        attempt_number = await self._repo.get_next_attempt_number(user_id, challenge_id)
        submission = await self._repo.create(
            user_id=user_id,
            challenge_id=challenge_id,
            answer=answer.strip(),
            attempt_number=attempt_number,
            evaluation_strategy_snapshot={"type": challenge.evaluation_strategy.get("type")},
        )
        await self._dispatcher.publish(
            submission_events.submission_created(
                submission.id, user_id, challenge_id, attempt_number
            )
        )
        await self._audit.record(
            actor_id=user_id,
            action="submission.created",
            resource="submission",
            metadata={
                "submissionId": str(submission.id),
                "challengeId": str(challenge_id),
                "attemptNumber": attempt_number,
            },
        )
        from app.modules.evaluations.application.evaluation_service import EvaluationService

        await EvaluationService(self._session, dispatcher=self._dispatcher).evaluate_submission(
            submission.id
        )
        refreshed = await self._repo.get_by_id(submission.id)
        return refreshed if refreshed is not None else submission

    async def get_submission(
        self, submission_id: UUID, *, requester_id: UUID, is_admin: bool
    ) -> Submission:
        submission = await self._repo.get_by_id(submission_id)
        if submission is None:
            raise SubmissionNotFoundError()
        if not is_admin and submission.user_id != requester_id:
            raise SubmissionAccessDeniedError()
        return submission

    async def list_my_submissions(
        self,
        user_id: UUID,
        *,
        page: int,
        page_size: int,
        challenge_id: UUID | None = None,
    ) -> tuple[list[Submission], int]:
        return await self._repo.list_by_user(
            user_id, page=page, page_size=page_size, challenge_id=challenge_id
        )

    async def list_submissions(
        self,
        *,
        page: int,
        page_size: int,
        user_id: UUID | None = None,
        challenge_id: UUID | None = None,
        status: SubmissionStatus | None = None,
    ) -> tuple[list[Submission], int]:
        return await self._repo.list_all(
            page=page,
            page_size=page_size,
            user_id=user_id,
            challenge_id=challenge_id,
            status=status,
        )

    async def update_submission_status(
        self,
        *,
        submission_id: UUID,
        status: SubmissionStatus,
        feedback: str | None = None,
        processing_time_ms: int | None = None,
    ) -> Submission:
        existing = await self._repo.get_by_id(submission_id)
        if existing is None:
            raise SubmissionNotFoundError()
        updated = await self._repo.update_status(
            submission_id,
            status=status,
            feedback=feedback,
            processing_time_ms=processing_time_ms,
        )
        if updated is None:
            raise SubmissionNotFoundError()
        await self._dispatcher.publish(
            submission_events.submission_updated_status(
                submission_id, status.value, existing.user_id, existing.challenge_id
            )
        )
        return updated

    async def get_submission_for_evaluation(self, submission_id: UUID) -> Submission:
        submission = await self._repo.get_by_id(submission_id)
        if submission is None:
            raise SubmissionNotFoundError()
        return submission
