from uuid import UUID

from app.shared.schemas.response import ApiModel


class TokenResponse(ApiModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RegisterResponse(ApiModel):
    user_id: UUID
    verification_required: bool
    tokens: TokenResponse | None = None
    verification_token: str | None = None


class SessionUserResponse(ApiModel):
    user_id: UUID
    email: str
    display_name: str
    role: str
    status: str


class MessageResponse(ApiModel):
    message: str
