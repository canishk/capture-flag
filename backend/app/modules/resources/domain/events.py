from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def resource_created(resource_id: UUID, title: str) -> DomainEvent:
    return DomainEvent(
        event_type="ResourceCreated",
        publisher="resources",
        aggregate_id=resource_id,
        aggregate_type="Resource",
        payload={"title": title},
    )


def resource_updated(resource_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ResourceUpdated",
        publisher="resources",
        aggregate_id=resource_id,
        aggregate_type="Resource",
        payload={},
    )


def resource_published(resource_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ResourcePublished",
        publisher="resources",
        aggregate_id=resource_id,
        aggregate_type="Resource",
        payload={},
    )


def resource_hidden(resource_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ResourceHidden",
        publisher="resources",
        aggregate_id=resource_id,
        aggregate_type="Resource",
        payload={},
    )


def resource_linked(resource_id: UUID, challenge_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="ResourceLinked",
        publisher="resources",
        aggregate_id=resource_id,
        aggregate_type="Resource",
        payload={"challengeId": str(challenge_id)},
    )
