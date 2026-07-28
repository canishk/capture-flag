from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def achievement_unlocked(achievement_id: UUID, user_id: UUID, achievement_code: str) -> DomainEvent:
    return DomainEvent(
        event_type="AchievementUnlocked",
        publisher="achievements",
        aggregate_id=achievement_id,
        aggregate_type="Achievement",
        payload={"userId": str(user_id), "achievementCode": achievement_code},
    )
