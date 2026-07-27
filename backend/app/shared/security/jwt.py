from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from jose import JWTError, jwt
from pydantic import BaseModel

from app.shared.config import get_settings
from app.shared.exceptions.base import UnauthorizedError


class TokenPayload(BaseModel):
    sub: UUID
    role: str
    jti: str
    exp: datetime
    iat: datetime
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


def create_access_token(*, user_id: UUID, role: str, jti: str) -> tuple[str, int]:
    settings = get_settings()
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    now = datetime.now(UTC)
    expire = now + expires_delta
    payload = {
        "sub": str(user_id),
        "role": role,
        "jti": jti,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "token_type": "access",
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, int(expires_delta.total_seconds())


def decode_access_token(token: str) -> TokenPayload:
    settings = get_settings()
    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("token_type") != "access":
            raise UnauthorizedError(message="Invalid token type")
        return TokenPayload(
            sub=UUID(payload["sub"]),
            role=payload["role"],
            jti=payload["jti"],
            exp=datetime.fromtimestamp(payload["exp"], tz=UTC),
            iat=datetime.fromtimestamp(payload["iat"], tz=UTC),
            token_type=payload["token_type"],
        )
    except (JWTError, KeyError, ValueError) as exc:
        raise UnauthorizedError(message="Invalid or expired token") from exc
