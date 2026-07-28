from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def trophy_awarded(trophy_id: UUID, user_id: UUID, trophy_code: str) -> DomainEvent:
    return DomainEvent(
        event_type="TrophyAwarded",
        publisher="trophies",
        aggregate_id=trophy_id,
        aggregate_type="Trophy",
        payload={"userId": str(user_id), "trophyCode": trophy_code},
    )
