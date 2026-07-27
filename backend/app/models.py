"""Import all ORM models for Alembic metadata registration."""

from app.modules.authentication.infrastructure.models import (  # noqa: F401
    CredentialModel,
    RefreshTokenModel,
    VerificationTokenModel,
)
from app.modules.categories.infrastructure.models import CategoryModel  # noqa: F401
from app.modules.challenges.infrastructure.models import ChallengeModel  # noqa: F401
from app.modules.hints.infrastructure.models import HintModel  # noqa: F401
from app.modules.levels.infrastructure.models import LevelModel  # noqa: F401
from app.modules.resources.infrastructure.models import (  # noqa: F401
    ChallengeResourceModel,
    ResourceModel,
)
from app.modules.users.infrastructure.models import UserModel  # noqa: F401
from app.shared.audit.models import AuditLogModel  # noqa: F401
from app.shared.database.base import Base

__all__ = ["Base"]
