"""Import all ORM models for Alembic metadata registration."""

from app.modules.achievements.infrastructure.models import (  # noqa: F401
    AchievementDefinitionModel,
    UserAchievementProgressModel,
)
from app.modules.authentication.infrastructure.models import (  # noqa: F401
    CredentialModel,
    RefreshTokenModel,
    VerificationTokenModel,
)
from app.modules.categories.infrastructure.models import CategoryModel  # noqa: F401
from app.modules.challenges.infrastructure.models import ChallengeModel  # noqa: F401
from app.modules.evaluations.infrastructure.models import EvaluationModel  # noqa: F401
from app.modules.hints.infrastructure.models import HintModel  # noqa: F401
from app.modules.leaderboards.infrastructure.models import LeaderboardEntryModel  # noqa: F401
from app.modules.levels.infrastructure.models import LevelModel  # noqa: F401
from app.modules.progress.infrastructure.models import (  # noqa: F401
    CategoryCompletionModel,
    ChallengeCompletionModel,
    LearnerProgressModel,
    LevelCompletionModel,
)
from app.modules.resources.infrastructure.models import (  # noqa: F401
    ChallengeResourceModel,
    ResourceModel,
)
from app.modules.submissions.infrastructure.models import SubmissionModel  # noqa: F401
from app.modules.trophies.infrastructure.models import (  # noqa: F401
    TrophyAwardModel,
    TrophyDefinitionModel,
)
from app.modules.users.infrastructure.models import UserModel  # noqa: F401
from app.shared.audit.models import AuditLogModel  # noqa: F401
from app.shared.database.base import Base
from app.shared.recognition.models import ProcessedRecognitionEventModel  # noqa: F401

__all__ = ["Base"]
