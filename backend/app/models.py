"""Import all ORM models for Alembic metadata registration."""

from app.modules.authentication.infrastructure.models import (  # noqa: F401
    CredentialModel,
    RefreshTokenModel,
    VerificationTokenModel,
)
from app.modules.users.infrastructure.models import UserModel  # noqa: F401
from app.shared.audit.models import AuditLogModel  # noqa: F401
from app.shared.database.base import Base

__all__ = ["Base"]
