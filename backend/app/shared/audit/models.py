from typing import Any
from uuid import UUID

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AuditLogModel(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "audit_log"

    actor_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(100), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, nullable=False, default=dict)
