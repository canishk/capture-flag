from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.users.domain.enums import UserRole, UserStatus
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class UserModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "user"

    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", native_enum=False),
        nullable=False,
        default=UserRole.LEARNER,
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status", native_enum=False),
        nullable=False,
        default=UserStatus.PENDING_VERIFICATION,
    )
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    preferences: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)

    credential: Mapped["CredentialModel"] = relationship(
        "CredentialModel",
        back_populates="user",
        uselist=False,
    )
