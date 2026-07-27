from uuid import UUID

from app.shared.events.dispatcher import DomainEvent


def evaluation_completed(
    evaluation_id: UUID,
    submission_id: UUID,
    user_id: UUID,
    challenge_id: UUID,
    passed: bool,
    score: int,
) -> DomainEvent:
    return DomainEvent(
        event_type="EvaluationCompleted",
        publisher="evaluations",
        aggregate_id=evaluation_id,
        aggregate_type="Evaluation",
        payload={
            "submissionId": str(submission_id),
            "userId": str(user_id),
            "challengeId": str(challenge_id),
            "passed": passed,
            "score": score,
        },
    )


def evaluation_failed(
    evaluation_id: UUID,
    submission_id: UUID,
    user_id: UUID,
    challenge_id: UUID,
    reason: str,
) -> DomainEvent:
    return DomainEvent(
        event_type="EvaluationFailed",
        publisher="evaluations",
        aggregate_id=evaluation_id,
        aggregate_type="Evaluation",
        payload={
            "submissionId": str(submission_id),
            "userId": str(user_id),
            "challengeId": str(challenge_id),
            "reason": reason,
        },
    )
