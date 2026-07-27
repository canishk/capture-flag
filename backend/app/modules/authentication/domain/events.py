from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def user_registered(user_id: UUID, email: str, display_name: str) -> DomainEvent:
    return DomainEvent(
        event_type="UserRegistered",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={"email": email, "displayName": display_name},
    )


def user_logged_in(user_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="UserLoggedIn",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={},
    )


def user_logged_out(user_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="UserLoggedOut",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={},
    )


def password_changed(user_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="PasswordChanged",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={},
    )


def password_reset_requested(user_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="PasswordResetRequested",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={},
    )


def email_verified(user_id: UUID) -> DomainEvent:
    return DomainEvent(
        event_type="EmailVerified",
        publisher="authentication",
        aggregate_id=user_id,
        aggregate_type="User",
        payload={},
    )
