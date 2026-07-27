from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.domain import events as user_events
from app.modules.users.domain.entities import UserProfile
from app.modules.users.domain.enums import UserRole, UserStatus
from app.modules.users.domain.exceptions import UserNotFoundError
from app.modules.users.infrastructure.repository import UserRepository
from app.shared.audit.service import AuditService
from app.shared.events.dispatcher import EventDispatcher, get_event_dispatcher


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        dispatcher: EventDispatcher | None = None,
    ) -> None:
        self._session = session
        self._repo = UserRepository(session)
        self._audit = AuditService(session)
        self._dispatcher = dispatcher or get_event_dispatcher()

    async def get_profile(self, user_id: UUID) -> UserProfile:
        user = await self._repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()
        return user

    async def update_profile(
        self,
        user_id: UUID,
        *,
        display_name: str | None = None,
        preferences: dict[str, Any] | None = None,
    ) -> UserProfile:
        user = await self._repo.update_profile(
            user_id,
            display_name=display_name,
            preferences=preferences,
        )
        await self._dispatcher.publish(
            user_events.user_profile_updated(user_id, displayName=user.display_name)
        )
        await self._audit.record(
            actor_id=user_id,
            action="user.profile_updated",
            resource="user",
            metadata={},
        )
        return user

    async def list_users(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[UserProfile], int]:
        return await self._repo.list_users(page=page, page_size=page_size, search=search)

    async def update_user_admin(
        self,
        *,
        actor_id: UUID,
        user_id: UUID,
        role: UserRole | None = None,
        status: UserStatus | None = None,
    ) -> UserProfile:
        user = await self.get_profile(user_id)
        if role is not None:
            user = await self._repo.update_role(user_id, role)
            await self._audit.record(
                actor_id=actor_id,
                action="user.role_changed",
                resource="user",
                metadata={"role": role.value},
            )
        if status is not None:
            user = await self._repo.update_status(user_id, status)
            if status == UserStatus.DISABLED:
                await self._dispatcher.publish(user_events.user_disabled(user_id))
                await self._audit.record(
                    actor_id=actor_id,
                    action="user.disabled",
                    resource="user",
                    metadata={},
                )
            elif status == UserStatus.ACTIVE:
                await self._dispatcher.publish(user_events.user_enabled(user_id))
                await self._audit.record(
                    actor_id=actor_id,
                    action="user.enabled",
                    resource="user",
                    metadata={},
                )
        return user

    async def set_avatar(self, user_id: UUID, avatar_url: str) -> UserProfile:
        user = await self._repo.update_profile(user_id, avatar_url=avatar_url)
        await self._audit.record(
            actor_id=user_id,
            action="user.avatar_changed",
            resource="user",
            metadata={},
        )
        return user

    async def clear_avatar(self, user_id: UUID) -> UserProfile:
        user = await self._repo.update_profile(user_id, clear_avatar=True)
        await self._audit.record(
            actor_id=user_id,
            action="user.avatar_removed",
            resource="user",
            metadata={},
        )
        return user
