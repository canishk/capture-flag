import hashlib
import secrets
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.domain.enums import UserRole, UserStatus
from app.modules.users.infrastructure.repository import UserRepository
from app.shared.database.dependencies import DbSession
from app.shared.exceptions.base import ForbiddenError, UnauthorizedError
from app.shared.security.jwt import TokenPayload, decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)


class CurrentUserContext:
    def __init__(self, user_id: UUID, role: UserRole, status: UserStatus, email: str) -> None:
        self.user_id = user_id
        self.role = role
        self.status = status
        self.email = email

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMINISTRATOR


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(DbSession),
) -> CurrentUserContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError(message="Authentication required")
    token_payload: TokenPayload = decode_access_token(credentials.credentials)
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id_with_credential(token_payload.sub)
    if user is None:
        raise UnauthorizedError(message="Invalid or expired token")
    if user.status == UserStatus.DISABLED:
        raise ForbiddenError(code="ACCOUNT_DISABLED", message="Account is disabled")
    return CurrentUserContext(
        user_id=user.id,
        role=user.role,
        status=user.status,
        email=user.email,
    )


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(DbSession),
) -> CurrentUserContext | None:
    if credentials is None:
        return None
    return await get_current_user(credentials, session)


def require_admin(current_user: CurrentUserContext = Depends(get_current_user)) -> CurrentUserContext:
    if not current_user.is_admin:
        raise ForbiddenError(code="ADMIN_REQUIRED", message="Administrator access required")
    return current_user


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_secure_token() -> str:
    return secrets.token_urlsafe(32)
