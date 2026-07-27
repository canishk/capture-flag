from enum import StrEnum


class UserRole(StrEnum):
    LEARNER = "learner"
    ADMINISTRATOR = "administrator"


class UserStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"
    PENDING_VERIFICATION = "pending_verification"
