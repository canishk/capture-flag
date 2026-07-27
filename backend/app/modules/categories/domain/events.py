from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def category_created(category_id: UUID, name: str) -> DomainEvent:
    return DomainEvent(
        event_type="CategoryCreated",
        publisher="categories",
        aggregate_id=category_id,
        aggregate_type="Category",
        payload={"name": name},
    )


def category_updated(category_id: UUID, name: str) -> DomainEvent:
    return DomainEvent(
        event_type="CategoryUpdated",
        publisher="categories",
        aggregate_id=category_id,
        aggregate_type="Category",
        payload={"name": name},
    )


def category_hidden(category_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="CategoryHidden",
        publisher="categories",
        aggregate_id=category_id,
        aggregate_type="Category",
        payload={},
    )
