from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def progress_updated(
    user_id: UUID,
    *,
    total_xp: int,
    challenges_completed: int,
    challenges_attempted: int,
    levels_completed: int,
    categories_completed: int,
    last_active_challenge_id: UUID | None,
) -> DomainEvent:
    return DomainEvent(
        event_type="ProgressUpdated",
        publisher="progress",
        aggregate_id=user_id,
        aggregate_type="LearnerProgress",
        payload={
            "userId": str(user_id),
            "totalXp": total_xp,
            "challengesCompleted": challenges_completed,
            "challengesAttempted": challenges_attempted,
            "levelsCompleted": levels_completed,
            "categoriesCompleted": categories_completed,
            "lastActiveChallengeId": str(last_active_challenge_id)
            if last_active_challenge_id
            else None,
        },
    )


def challenge_completed(user_id: UUID, challenge_id: UUID, score: int) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengeCompleted",
        publisher="progress",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={"userId": str(user_id), "challengeId": str(challenge_id), "score": score},
    )


def level_completed(user_id: UUID, level_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="LevelCompleted",
        publisher="progress",
        aggregate_id=level_id,
        aggregate_type="Level",
        payload={"userId": str(user_id), "levelId": str(level_id)},
    )


def category_completed(user_id: UUID, category_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="CategoryCompleted",
        publisher="progress",
        aggregate_id=category_id,
        aggregate_type="Category",
        payload={"userId": str(user_id), "categoryId": str(category_id)},
    )
