from typing import Any, Protocol
from uuid import UUID

from app.modules.hints.domain.entities import Hint
from app.modules.hints.domain.enums import HintStatus


class HintRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        challenge_id: UUID,
        title: str,
        content: str,
        display_order: int,
        penalty_config: dict[str, Any],
        unlock_config: dict[str, Any],
        status: HintStatus,
    ) -> Hint: ...

    async def get_by_id(self, hint_id: UUID) -> Hint | None: ...

    async def list_by_challenge(
        self,
        challenge_id: UUID,
        *,
        page: int,
        page_size: int,
        status: HintStatus | None = None,
    ) -> tuple[list[Hint], int]: ...

    async def update(self, hint_id: UUID, **kwargs: Any) -> Hint | None: ...

    async def update_display_order(self, hint_id: UUID, display_order: int) -> Hint | None: ...

    async def get_max_display_order(self, challenge_id: UUID) -> int: ...

    async def order_exists(self, challenge_id: UUID, display_order: int, exclude_id: UUID | None = None) -> bool: ...
