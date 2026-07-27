from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func

from app.modules.authentication.infrastructure.models import CredentialModel
from app.modules.users.domain.entities import UserProfile
from app.modules.users.domain.enums import UserRole, UserStatus
from app.modules.users.infrastructure.models import UserModel


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        *,
        user_id: UUID,
        email: str,
        password_hash: str,
        display_name: str,
        status: UserStatus,
        role: UserRole = UserRole.LEARNER,
    ) -> UserProfile:
        user = UserModel(
            id=user_id,
            display_name=display_name,
            role=role,
            status=status,
            preferences={},
        )
        now = datetime.now(UTC)
        credential = CredentialModel(
            user_id=user_id,
            email=email.lower(),
            password_hash=password_hash,
            email_verified_at=None,
            created_at=now,
            updated_at=now,
        )
        self._session.add(user)
        self._session.add(credential)
        await self._session.flush()
        return self._to_entity(user, credential.email)

    async def get_by_id(self, user_id: UUID) -> UserProfile | None:
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.credential))
            .where(UserModel.id == user_id)
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or user.credential is None:
            return None
        return self._to_entity(user, user.credential.email)

    async def get_by_id_with_credential(self, user_id: UUID) -> UserProfile | None:
        return await self.get_by_id(user_id)

    async def get_by_email(self, email: str) -> UserProfile | None:
        stmt = (
            select(UserModel)
            .join(CredentialModel, CredentialModel.user_id == UserModel.id)
            .options(selectinload(UserModel.credential))
            .where(CredentialModel.email == email.lower())
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or user.credential is None:
            return None
        return self._to_entity(user, user.credential.email)

    async def list_users(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[UserProfile], int]:
        stmt = select(UserModel).options(selectinload(UserModel.credential))
        if search:
            pattern = f"%{search}%"
            stmt = stmt.join(CredentialModel).where(
                (UserModel.display_name.ilike(pattern))
                | (CredentialModel.email.ilike(pattern))
            )
            count_stmt = (
                select(func.count())
                .select_from(UserModel)
                .join(CredentialModel)
                .where(
                    (UserModel.display_name.ilike(pattern))
                    | (CredentialModel.email.ilike(pattern))
                )
            )
        else:
            count_stmt = select(func.count()).select_from(UserModel)
        total = await self._session.scalar(count_stmt)
        stmt = stmt.order_by(UserModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        profiles = [
            self._to_entity(user, user.credential.email)
            for user in users
            if user.credential is not None
        ]
        return profiles, int(total or 0)

    async def update_profile(
        self,
        user_id: UUID,
        *,
        display_name: str | None = None,
        preferences: dict | None = None,
        avatar_url: str | None = None,
        clear_avatar: bool = False,
    ) -> UserProfile:
        user = await self._get_model(user_id)
        if display_name is not None:
            user.display_name = display_name
        if preferences is not None:
            user.preferences = preferences
        if clear_avatar:
            user.avatar_url = None
        elif avatar_url is not None:
            user.avatar_url = avatar_url
        await self._session.flush()
        await self._session.refresh(user, attribute_names=["credential"])
        return self._to_entity(user, user.credential.email)

    async def update_role(self, user_id: UUID, role: UserRole) -> UserProfile:
        user = await self._get_model(user_id)
        user.role = role
        await self._session.flush()
        return self._to_entity(user, user.credential.email)

    async def update_status(self, user_id: UUID, status: UserStatus) -> UserProfile:
        user = await self._get_model(user_id)
        user.status = status
        await self._session.flush()
        return self._to_entity(user, user.credential.email)

    async def _get_model(self, user_id: UUID) -> UserModel:
        stmt = (
            select(UserModel)
            .options(selectinload(UserModel.credential))
            .where(UserModel.id == user_id)
        )
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None or user.credential is None:
            from app.modules.users.domain.exceptions import UserNotFoundError

            raise UserNotFoundError()
        return user

    @staticmethod
    def _to_entity(user: UserModel, email: str) -> UserProfile:
        return UserProfile(
            id=user.id,
            email=email,
            display_name=user.display_name,
            role=user.role,
            status=user.status,
            avatar_url=user.avatar_url,
            preferences=user.preferences,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
