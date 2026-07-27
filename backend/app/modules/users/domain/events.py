from app.shared.events.dispatcher import DomainEvent


def user_profile_updated(user_id, **payload) -> DomainEvent:
    from uuid import UUID

    return DomainEvent(
        event_type="UserProfileUpdated",
        publisher="users",
        aggregate_id=user_id if isinstance(user_id, UUID) else UUID(str(user_id)),
        aggregate_type="User",
        payload=payload,
    )


def user_disabled(user_id) -> DomainEvent:
    from uuid import UUID

    return DomainEvent(
        event_type="UserDisabled",
        publisher="users",
        aggregate_id=user_id if isinstance(user_id, UUID) else UUID(str(user_id)),
        aggregate_type="User",
        payload={},
    )


def user_enabled(user_id) -> DomainEvent:
    from uuid import UUID

    return DomainEvent(
        event_type="UserEnabled",
        publisher="users",
        aggregate_id=user_id if isinstance(user_id, UUID) else UUID(str(user_id)),
        aggregate_type="User",
        payload={},
    )
