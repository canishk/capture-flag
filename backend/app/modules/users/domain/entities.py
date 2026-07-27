from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.users.domain.enums import UserRole, UserStatus


@dataclass
class UserProfile:
    id: UUID
    email: str
    display_name: str
    role: UserRole
    status: UserStatus
    avatar_url: str | None
    preferences: dict[str, Any]
    created_at: datetime
    updated_at: datetime
