from enum import StrEnum


class TrophyTriggerType(StrEnum):
    FIRST_CHALLENGE = "first_challenge"
    CHALLENGE_COMPLETED = "challenge_completed"
    LEVEL_COMPLETED = "level_completed"
    CATEGORY_COMPLETED = "category_completed"
