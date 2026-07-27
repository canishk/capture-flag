from typing import Protocol
from uuid import UUID

from app.modules.categories.domain.entities import Category
from app.modules.categories.domain.enums import CategoryStatus


class CategoryRepositoryProtocol(Protocol):
    async def create(
        self,
        *,
        name: str,
        description: str | None,
        icon: str,
        display_order: int,
        status: CategoryStatus,
    ) -> Category: ...

    async def get_by_id(self, category_id: UUID) -> Category | None: ...

    async def get_by_name(self, name: str) -> Category | None: ...

    async def list_categories(
        self,
        *,
        page: int,
        page_size: int,
        status: CategoryStatus | None = None,
        search: str | None = None,
    ) -> tuple[list[Category], int]: ...

    async def update(
        self,
        category_id: UUID,
        *,
        name: str | None = None,
        description: str | None = None,
        icon: str | None = None,
        status: CategoryStatus | None = None,
    ) -> Category | None: ...

    async def update_display_order(self, category_id: UUID, display_order: int) -> Category | None: ...

    async def get_max_display_order(self) -> int: ...
