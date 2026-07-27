from typing import Any, Protocol
from uuid import UUID

from app.modules.evaluations.domain.entities import Evaluation


class EvaluationRepositoryProtocol(Protocol):
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
    ) -> Evaluation: ...

    async def get_by_submission_id(self, submission_id: UUID) -> Evaluation | None: ...

    async def get_by_id(self, evaluation_id: UUID) -> Evaluation | None: ...
