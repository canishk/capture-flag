from __future__ import annotations

from uuid import UUID

from sqlalchemy import JSON, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.resources.domain.enums import ResourceStatus, ResourceType
from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class ResourceModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "resource"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(String(500), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    resource_type: Mapped[ResourceType] = mapped_column(
        Enum(ResourceType, name="resource_type", native_enum=False),
        nullable=False,
        index=True,
    )
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source: Mapped[str | None] = mapped_column(String(200), nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    status: Mapped[ResourceStatus] = mapped_column(
        Enum(ResourceStatus, name="resource_status", native_enum=False),
        nullable=False,
        default=ResourceStatus.DRAFT,
        index=True,
    )


class ChallengeResourceModel(Base):
    __tablename__ = "challenge_resource"

    challenge_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("challenge.id", ondelete="CASCADE"),
        primary_key=True,
    )
    resource_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("resource.id", ondelete="CASCADE"),
        primary_key=True,
    )
