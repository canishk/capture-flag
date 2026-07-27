from datetime import datetime
from uuid import UUID

from app.modules.categories.domain.entities import Category
from app.shared.schemas.response import ApiModel


class CategoryResponse(ApiModel):
    id: UUID
    name: str
    description: str | None
    icon: str
    display_order: int
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, category: Category) -> "CategoryResponse":
        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            icon=category.icon,
            display_order=category.display_order,
            status=category.status.value,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
