from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def submission_created(
    submission_id: UUID, user_id: UUID, challenge_id: UUID, attempt_number: int
) -> DomainEvent:
    return DomainEvent(
        event_type="SubmissionCreated",
        publisher="submissions",
        aggregate_id=submission_id,
        aggregate_type="Submission",
        payload={
            "userId": str(user_id),
            "challengeId": str(challenge_id),
            "attemptNumber": attempt_number,
        },
    )


def submission_updated_status(
    submission_id: UUID, status: str, user_id: UUID, challenge_id: UUID
) -> DomainEvent:
    return DomainEvent(
        event_type="SubmissionUpdatedStatus",
        publisher="submissions",
        aggregate_id=submission_id,
        aggregate_type="Submission",
        payload={
            "status": status,
            "userId": str(user_id),
            "challengeId": str(challenge_id),
        },
    )
