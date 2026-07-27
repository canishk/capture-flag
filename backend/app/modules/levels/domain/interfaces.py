from typing import Any, Protocol
from uuid import UUID

from app.modules.levels.domain.entities import Level
from app.modules.levels.domain.enums import LevelStatus


class LevelRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        category_id: UUID,
        name: str,
        description: str | None,
        display_order: int,
        status: LevelStatus,
        unlock_config: dict[str, Any],
    ) -> Level: ...

    async def get_by_id(self, level_id: UUID) -> Level | None: ...

    async def list_by_category(
        self,
        category_id: UUID,
        *,
        page: int,
        page_size: int,
        status: LevelStatus | None = None,
    ) -> tuple[list[Level], int]: ...

    async def list_all(
        self,
        *,
        page: int,
        page_size: int,
        status: LevelStatus | None = None,
    ) -> tuple[list[Level], int]: ...

    async def update(
        self,
        level_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        status: LevelStatus | None = None,
        unlock_config: dict[str, Any] | None = None,
    ) -> Level | None: ...

    async def update_display_order(self, level_id: UUID, display_order: int) -> Level | None: ...

    async def get_max_display_order(self, category_id: UUID) -> int: ...

    async def exists_in_category(self, level_id: UUID, category_id: UUID) -> bool: ...
