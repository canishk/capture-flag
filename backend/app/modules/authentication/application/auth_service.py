from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.authentication.application.password_service import (
    hash_password,
    validate_password_strength,
    verify_password,
)
from app.modules.authentication.domain import events as auth_events
from app.modules.authentication.domain.exceptions import (
    EmailAlreadyRegisteredError,
    EmailNotVerifiedError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.modules.authentication.infrastructure.models import VerificationTokenType
from app.modules.authentication.infrastructure.repository import AuthRepository
from app.modules.users.domain.enums import UserRole, UserStatus
from app.modules.users.infrastructure.repository import UserRepository
from app.shared.audit.service import AuditService
from app.shared.config import get_settings
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher
from app.shared.security.jwt import TokenPair, create_access_token


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._auth_repo = AuthRepository(session)
        self._user_repo = UserRepository(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()
        self._settings = get_settings()

    async def register(
        self,
        *,
        email: str,
        password: str,
        display_name: str,
    ) -> tuple[UUID, TokenPair | None, str | None]:
        validate_password_strength(password)
        existing = await self._auth_repo.get_credential_by_email(email)
        if existing is not None:
            raise EmailAlreadyRegisteredError()

        user_id = uuid4()
        status = (
            UserStatus.PENDING_VERIFICATION
            if self._settings.email_verification_required
            else UserStatus.ACTIVE
        )
        password_hash = hash_password(password)
        await self._user_repo.create(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            status=status,
        )

        verification_token: str | None = None
        if self._settings.email_verification_required:
            verification_token = await self._auth_repo.create_verification_token(
                user_id=user_id,
                token_type=VerificationTokenType.EMAIL_VERIFICATION,
                expires_at=datetime.now(UTC)
                + timedelta(hours=self._settings.email_verification_token_expire_hours),
            )
            tokens = None
        else:
            await self._auth_repo.mark_email_verified(user_id)
            tokens = await self._issue_tokens(user_id=user_id, role=UserRole.LEARNER)

        await self._dispatcher.publish(
            auth_events.user_registered(user_id, email=email, display_name=display_name)
        )
        await self._audit.record(
            actor_id=user_id,
            action="user.registered",
            resource="user",
            metadata={"email": email},
        )
        return user_id, tokens, verification_token

    async def login(self, *, email: str, password: str) -> TokenPair:
        credential = await self._auth_repo.get_credential_by_email(email)
        if credential is None or not verify_password(credential.password_hash, password):
            await self._audit.record(
                actor_id=None,
                action="auth.login_failed",
                resource="credential",
                metadata={"email": email.lower()},
            )
            raise InvalidCredentialsError()

        user = await self._user_repo.get_by_id(credential.user_id)
        if user is None:
            raise InvalidCredentialsError()

        if user.status == UserStatus.DISABLED:
            raise InvalidCredentialsError()

        if self._settings.email_verification_required and credential.email_verified_at is None:
            raise EmailNotVerifiedError()

        if user.status == UserStatus.PENDING_VERIFICATION and credential.email_verified_at is not None:
            await self._user_repo.update_status(user.id, UserStatus.ACTIVE)

        tokens = await self._issue_tokens(user_id=user.id, role=user.role)
        await self._dispatcher.publish(auth_events.user_logged_in(user.id))
        await self._audit.record(
            actor_id=user.id,
            action="auth.login_succeeded",
            resource="user",
            metadata={},
        )
        return tokens

    async def logout(self, *, user_id: UUID, refresh_token: str | None) -> None:
        if refresh_token:
            stored = await self._auth_repo.get_valid_refresh_token(refresh_token)
            if stored is not None:
                await self._auth_repo.revoke_refresh_token(stored.id)
        await self._dispatcher.publish(auth_events.user_logged_out(user_id))
        await self._audit.record(
            actor_id=user_id,
            action="auth.logout",
            resource="user",
            metadata={},
        )

    async def refresh(self, *, refresh_token: str) -> TokenPair:
        stored = await self._auth_repo.get_valid_refresh_token(refresh_token)
        if stored is None:
            raise InvalidTokenError(message="Invalid or expired refresh token")

        user = await self._user_repo.get_by_id(stored.user_id)
        if user is None or user.status == UserStatus.DISABLED:
            raise InvalidTokenError(message="Invalid or expired refresh token")

        await self._auth_repo.revoke_refresh_token(stored.id)
        return await self._issue_tokens(user_id=user.id, role=user.role)

    async def change_password(
        self,
        *,
        user_id: UUID,
        current_password: str,
        new_password: str,
    ) -> None:
        validate_password_strength(new_password)
        credential = await self._auth_repo.get_credential_by_user_id(user_id)
        if credential is None or not verify_password(credential.password_hash, current_password):
            raise InvalidCredentialsError()

        await self._auth_repo.update_password_hash(user_id, hash_password(new_password))
        await self._auth_repo.revoke_all_refresh_tokens(user_id)
        await self._dispatcher.publish(auth_events.password_changed(user_id))
        await self._audit.record(
            actor_id=user_id,
            action="auth.password_changed",
            resource="user",
            metadata={},
        )

    async def request_password_reset(self, *, email: str) -> str | None:
        credential = await self._auth_repo.get_credential_by_email(email)
        if credential is None:
            return None

        token = await self._auth_repo.create_verification_token(
            user_id=credential.user_id,
            token_type=VerificationTokenType.PASSWORD_RESET,
            expires_at=datetime.now(UTC)
            + timedelta(hours=self._settings.password_reset_token_expire_hours),
        )
        await self._dispatcher.publish(auth_events.password_reset_requested(credential.user_id))
        await self._audit.record(
            actor_id=credential.user_id,
            action="auth.password_reset_requested",
            resource="user",
            metadata={},
        )
        return token

    async def reset_password(self, *, token: str, new_password: str) -> None:
        validate_password_strength(new_password)
        user_id = await self._auth_repo.consume_verification_token(
            raw_token=token,
            token_type=VerificationTokenType.PASSWORD_RESET,
        )
        await self._auth_repo.update_password_hash(user_id, hash_password(new_password))
        await self._auth_repo.revoke_all_refresh_tokens(user_id)
        await self._dispatcher.publish(auth_events.password_changed(user_id))
        await self._audit.record(
            actor_id=user_id,
            action="auth.password_reset_completed",
            resource="user",
            metadata={},
        )

    async def verify_email(self, *, token: str) -> None:
        user_id = await self._auth_repo.consume_verification_token(
            raw_token=token,
            token_type=VerificationTokenType.EMAIL_VERIFICATION,
        )
        await self._auth_repo.mark_email_verified(user_id)
        await self._user_repo.update_status(user_id, UserStatus.ACTIVE)
        await self._dispatcher.publish(auth_events.email_verified(user_id))
        await self._audit.record(
            actor_id=user_id,
            action="auth.email_verified",
            resource="user",
            metadata={},
        )

    async def revoke_tokens_for_user(self, user_id: UUID) -> None:
        await self._auth_repo.revoke_all_refresh_tokens(user_id)

    async def _issue_tokens(self, *, user_id: UUID, role: UserRole) -> TokenPair:
        jti = str(uuid4())
        access_token, expires_in = create_access_token(
            user_id=user_id,
            role=role.value,
            jti=jti,
        )
        refresh_token = await self._auth_repo.create_refresh_token(
            user_id=user_id,
            expires_at=datetime.now(UTC) + timedelta(days=self._settings.refresh_token_expire_days),
        )
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
        )
