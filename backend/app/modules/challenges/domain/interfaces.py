from typing import Any, Protocol
from uuid import UUID

from app.modules.challenges.domain.entities import Challenge
from app.modules.challenges.domain.enums import (
    ChallengeDifficulty,
    ChallengeStatus,
    ChallengeType,
)


class ChallengeRepositoryProtocol(Protocol):
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
    ) -> Challenge: ...

    async def get_by_id(self, challenge_id: UUID) -> Challenge | None: ...

    async def get_by_title_in_level(self, level_id: UUID, title: str) -> Challenge | None: ...

    async def list_challenges(
        self,
        *,
        page: int,
        page_size: int,
        status: ChallengeStatus | None = None,
        category_id: UUID | None = None,
        level_id: UUID | None = None,
        search: str | None = None,
    ) -> tuple[list[Challenge], int]: ...

    async def update(
        self,
        challenge_id: UUID,
        **kwargs: Any,
    ) -> Challenge | None: ...

    async def update_display_order(self, challenge_id: UUID, display_order: int) -> Challenge | None: ...

    async def get_max_display_order(self, level_id: UUID) -> int: ...
