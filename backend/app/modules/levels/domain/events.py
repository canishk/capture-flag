from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def level_created(level_id: UUID, category_id: UUID, name: str) -> DomainEvent:
    return DomainEvent(
        event_type="LevelCreated",
        publisher="levels",
        aggregate_id=level_id,
        aggregate_type="Level",
        payload={"categoryId": str(category_id), "name": name},
    )


def level_updated(level_id: UUID, category_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="LevelUpdated",
        publisher="levels",
        aggregate_id=level_id,
        aggregate_type="Level",
        payload={"categoryId": str(category_id)},
    )


def level_hidden(level_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="LevelHidden",
        publisher="levels",
        aggregate_id=level_id,
        aggregate_type="Level",
        payload={},
    )
