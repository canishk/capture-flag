from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def challenge_created(challenge_id: UUID, level_id: UUID, title: str) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengeCreated",
        publisher="challenges",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={"levelId": str(level_id), "title": title},
    )


def challenge_updated(challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengeUpdated",
        publisher="challenges",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={},
    )


def challenge_published(challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengePublished",
        publisher="challenges",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={},
    )


def challenge_hidden(challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengeHidden",
        publisher="challenges",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={},
    )


def challenge_archived(challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ChallengeArchived",
        publisher="challenges",
        aggregate_id=challenge_id,
        aggregate_type="Challenge",
        payload={},
    )
