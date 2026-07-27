from typing import Any, Protocol
from uuid import UUID

from app.modules.submissions.domain.entities import Submission
from app.modules.submissions.domain.enums import SubmissionStatus


class SubmissionRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        user_id: UUID,
        challenge_id: UUID,
        answer: str,
        attempt_number: int,
        evaluation_strategy_snapshot: dict[str, Any],
    ) -> Submission: ...

    async def get_by_id(self, submission_id: UUID) -> Submission | None: ...

    async def get_next_attempt_number(self, user_id: UUID, challenge_id: UUID) -> int: ...

    async def list_by_user(
        self,
        user_id: UUID,
        *,
        page: int,
        page_size: int,
        challenge_id: UUID | None = None,
    ) -> tuple[list[Submission], int]: ...

    async def list_all(
        self,
        *,
        page: int,
        page_size: int,
        user_id: UUID | None = None,
        challenge_id: UUID | None = None,
        status: SubmissionStatus | None = None,
    ) -> tuple[list[Submission], int]: ...

    async def update_status(
        self,
        submission_id: UUID,
        *,
        status: SubmissionStatus,
        feedback: str | None = None,
        processing_time_ms: int | None = None,
    ) -> Submission | None: ...
