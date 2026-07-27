from enum import StrEnum


class ChallengeStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ChallengeType(StrEnum):
    TEXT_ANSWER = "text_answer"
    AI_CONVERSATION = "ai_conversation"
    EXTERNAL_WEBSITE = "external_website"


class ChallengeDifficulty(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"
