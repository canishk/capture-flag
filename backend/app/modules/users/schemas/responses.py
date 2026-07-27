from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.users.domain.entities import UserProfile
from app.shared.schemas.response import ApiModel


class UserResponse(ApiModel):
    id: UUID
    email: str
    display_name: str
    role: str
    status: str
    avatar_url: str | None
    preferences: dict[str, Any]
    joined_at: datetime

    @classmethod
    def from_entity(cls, user: UserProfile) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            role=user.role.value,
            status=user.status.value,
            avatar_url=user.avatar_url,
            preferences=user.preferences,
            joined_at=user.created_at,
        )


class PublicUserResponse(ApiModel):
    id: UUID
    display_name: str
    avatar_url: str | None
    role: str

    @classmethod
    def from_entity(cls, user: UserProfile) -> "PublicUserResponse":
        return cls(
            id=user.id,
            display_name=user.display_name,
            avatar_url=user.avatar_url,
            role=user.role.value,
        )
