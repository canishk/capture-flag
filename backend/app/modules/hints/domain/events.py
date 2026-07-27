from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def hint_created(hint_id: UUID, challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="HintCreated",
        publisher="hints",
        aggregate_id=hint_id,
        aggregate_type="Hint",
        payload={"challengeId": str(challenge_id)},
    )


def hint_updated(hint_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="HintUpdated",
        publisher="hints",
        aggregate_id=hint_id,
        aggregate_type="Hint",
        payload={},
    )


def hint_published(hint_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="HintPublished",
        publisher="hints",
        aggregate_id=hint_id,
        aggregate_type="Hint",
        payload={},
    )


def hint_hidden(hint_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="HintHidden",
        publisher="hints",
        aggregate_id=hint_id,
        aggregate_type="Hint",
        payload={},
    )
