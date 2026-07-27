from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.categories.domain.enums import CategoryStatus


@dataclass
class Category:
    id: UUID
    name: str
    description: str | None
    icon: str
    display_order: int
    status: CategoryStatus
    created_at: datetime
    updated_at: datetime
