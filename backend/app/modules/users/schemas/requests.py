from typing import Any

from pydantic import Field

from app.shared.schemas.response import ApiModel


class UpdateProfileRequest(ApiModel):
    display_name: str | None = Field(default=None, min_length=2, max_length=100)
    preferences: dict[str, Any] | None = None


class AdminUpdateUserRequest(ApiModel):
    role: str | None = None
    status: str | None = None
