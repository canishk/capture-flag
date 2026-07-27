from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.authentication.domain.exceptions import InvalidTokenError
from app.modules.authentication.infrastructure.models import (
    CredentialModel,
    RefreshTokenModel,
    VerificationTokenModel,
    VerificationTokenType,
)
from app.shared.security.dependencies import generate_secure_token, hash_token


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_credential_by_email(self, email: str) -> CredentialModel | None:
        stmt = select(CredentialModel).where(CredentialModel.email == email.lower())
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_credential_by_user_id(self, user_id: UUID) -> CredentialModel | None:
        stmt = select(CredentialModel).where(CredentialModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_password_hash(self, user_id: UUID, password_hash: str) -> None:
        stmt = (
            update(CredentialModel)
            .where(CredentialModel.user_id == user_id)
            .values(password_hash=password_hash, updated_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def mark_email_verified(self, user_id: UUID) -> None:
        stmt = (
            update(CredentialModel)
            .where(CredentialModel.user_id == user_id)
            .values(email_verified_at=datetime.now(UTC), updated_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def create_refresh_token(self, user_id: UUID, expires_at: datetime) -> str:
        raw_token = generate_secure_token()
        token = RefreshTokenModel(
            user_id=user_id,
            token_hash=hash_token(raw_token),
            expires_at=expires_at,
        )
        self._session.add(token)
        await self._session.flush()
        return raw_token

    async def get_valid_refresh_token(self, raw_token: str) -> RefreshTokenModel | None:
        token_hash = hash_token(raw_token)
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash,
            RefreshTokenModel.revoked_at.is_(None),
            RefreshTokenModel.expires_at > datetime.now(UTC),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token_id: UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def revoke_all_refresh_tokens(self, user_id: UUID) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.revoked_at.is_(None),
            )
            .values(revoked_at=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def create_verification_token(
        self,
        *,
        user_id: UUID,
        token_type: VerificationTokenType,
        expires_at: datetime,
    ) -> str:
        raw_token = generate_secure_token()
        token = VerificationTokenModel(
            user_id=user_id,
            token_hash=hash_token(raw_token),
            token_type=token_type,
            expires_at=expires_at,
        )
        self._session.add(token)
        await self._session.flush()
        return raw_token

    async def consume_verification_token(
        self,
        *,
        raw_token: str,
        token_type: VerificationTokenType,
    ) -> UUID:
        token_hash = hash_token(raw_token)
        stmt = select(VerificationTokenModel).where(
            VerificationTokenModel.token_hash == token_hash,
            VerificationTokenModel.token_type == token_type,
            VerificationTokenModel.used_at.is_(None),
            VerificationTokenModel.expires_at > datetime.now(UTC),
        )
        result = await self._session.execute(stmt)
        token = result.scalar_one_or_none()
        if token is None:
            raise InvalidTokenError()
        token.used_at = datetime.now(UTC)
        await self._session.flush()
        return token.user_id
