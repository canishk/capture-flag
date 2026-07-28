# ADR-005: Recognition Event Contracts

- Status: Accepted
- Date: 2026-07-27
- Authors: CipherForge Architecture Team
- Decision Type: Architecture / Integration

Related ADRs:
- ADR-001 — Adopt a Modular Monolith Architecture
- ADR-002 — Establish Domain Boundaries and Module Ownership
- ADR-003 — Repository Ownership and Data Access Rules
- ADR-004 — Adopt CQRS and Event-Driven Architecture

---

# Context

Sprint 3 introduced the complete learning workflow:

```
Challenge
    ↓
Submission
    ↓
Evaluation
    ↓
Progress Projection
```

Sprint 4 introduces the Recognition domain:

- Trophies
- Achievements
- Leaderboards
- Streaks
- Future notifications
- Analytics

Recognition must **not** couple directly to the Learning Workflow.

Instead, Recognition consumes published domain events.

This ADR defines those contracts.

---

# Decision

The Learning Workflow publishes stable domain events.

Recognition modules consume those events.

Recognition never writes back into:

- Submission
- Evaluation
- Progress

Recognition owns only recognition state.

---

# Event Ownership

| Event | Owner |
|---------|-------|
| SubmissionCreated | Submission |
| SubmissionStatusChanged | Submission |
| EvaluationCompleted | Evaluation |
| EvaluationFailed | Evaluation |
| ProgressUpdated | Progress |
| ChallengeCompleted | Progress |
| LevelCompleted | Progress |
| CategoryCompleted | Progress |

Only the owning module may publish these events.

No other module may publish an event with the same semantic meaning.

---

# Event Flow

```
Submission

↓

Evaluation

↓

Progress

↓

ChallengeCompleted
ProgressUpdated
LevelCompleted
CategoryCompleted

↓

Recognition

↓

Leaderboards
Trophies
Achievements
Notifications
Analytics
```

Recognition is downstream only.

---

# Event Versioning

Every published event contains:

```json
{
  "event_id": "uuid",
  "event_version": 1,
  "event_type": "...",
  "occurred_at": "...",
  "producer": "...",
  "payload": { }
}
```

Rules

- Version numbers are integers.
- Events are immutable.
- Consumers must tolerate unknown fields.
- Existing fields must not change meaning.
- Breaking changes require a new version.

Example:

```
ChallengeCompleted v1

↓

ChallengeCompleted v2
```

Never mutate v1.

---

# Event Metadata

Every event contains:

| Field | Required |
|---------|----------|
| event_id | Yes |
| event_version | Yes |
| event_type | Yes |
| occurred_at | Yes |
| producer | Yes |
| correlation_id | Recommended |
| causation_id | Recommended |
| payload | Yes |

---

# ChallengeCompleted

Producer:

Progress

Meaning:

The learner has successfully completed a challenge.

Payload:

```json
{
  "user_id": "...",
  "challenge_id": "...",
  "level_id": "...",
  "category_id": "...",
  "xp_awarded": 25,
  "completed_at": "..."
}
```

Consumers:

- Trophy Service
- Leaderboard Service
- Notification Service
- Analytics

---

# LevelCompleted

Producer:

Progress

Payload:

```json
{
  "user_id": "...",
  "level_id": "...",
  "category_id": "...",
  "completed_at": "..."
}
```

Consumers:

- Trophy Service
- Analytics

---

# CategoryCompleted

Producer:

Progress

Payload:

```json
{
  "user_id": "...",
  "category_id": "...",
  "completed_at": "..."
}
```

Consumers:

- Trophy Service
- Analytics

---

# ProgressUpdated

Producer:

Progress

Meaning

Projection state has changed.

Payload:

```json
{
  "user_id": "...",
  "xp": 250,
  "completed_challenges": 18,
  "completed_levels": 4,
  "completed_categories": 1,
  "resume_challenge_id": "...",
  "updated_at": "..."
}
```

Consumers:

- Dashboard
- Leaderboards
- Notifications
- Analytics

---

# Consumer Rules

Consumers must:

- Treat events as immutable.
- Process events independently.
- Remain idempotent.
- Ignore unknown fields.
- Never assume ordering beyond a single aggregate.
- Never modify producer state.

Consumers must not:

- Query producer repositories directly.
- Depend on internal implementation details.
- Trigger business logic in producer modules.

---

# Idempotency

Every consumer stores processed event identifiers.

```
event_id

↓

Already processed?

↓

Yes → Ignore

↓

No → Process
```

Replaying an event must not create duplicate trophies, leaderboard entries, or notifications.

---

# Ordering

Ordering is guaranteed only within a logical aggregate (for example, a single user's progress).

Consumers must not rely on global ordering across unrelated users or aggregates.

When ordering matters, use:

- occurred_at
- event_version
- aggregate identifier

---

# Error Handling

Consumer failures must not roll back the originating transaction.

If a consumer cannot process an event:

1. Log the failure.
2. Retry according to platform policy.
3. Move permanently failing events to a dead-letter mechanism (future enhancement).
4. Alert administrators when retries are exhausted.

---

# Transaction Boundary

The producer transaction is:

```
Create Submission

↓

Evaluate

↓

Update Progress

↓

Commit

↓

Publish Events
```

Events must never be published before the transaction commits successfully.

Future implementations may use the Outbox Pattern without changing event contracts.

---

# Repository Ownership

Recognition modules must never access repositories owned by:

- Submission
- Evaluation
- Progress

Recognition reads only:

- Event payloads
- Public APIs (when explicitly documented)

---

# Security

Events must not expose:

- Correct answers
- Hidden evaluation details
- Internal scoring algorithms
- Sensitive user information
- Authentication data
- Administrative metadata

Payloads should include only the data required by downstream consumers.

---

# Performance

Event payloads should be:

- Small
- Self-contained
- Stable
- Serializable

Large collections should never be embedded.

Consumers requiring additional information should retrieve it through documented public interfaces.

---

# Future Consumers

The following modules are expected to subscribe to these events:

- Trophy Service
- Achievement Engine
- Leaderboard Service
- Notification Service
- Activity Feed
- Analytics
- Recommendation Engine
- AI Coach

No changes to producer modules should be required to support these consumers.

---

# Consequences

## Positive

- Loose coupling between domains.
- Independent evolution of Recognition.
- Stable event contracts.
- Easier testing.
- Supports asynchronous processing.
- Compatible with the Outbox Pattern.
- Enables future microservice extraction.

## Trade-offs

- Event versioning must be maintained.
- Consumers must implement idempotency.
- Additional operational complexity for retries and monitoring.
- Eventual consistency between producer and consumer state.

---

# Acceptance Criteria

This ADR is satisfied when:

- Only producer modules publish their own events.
- Recognition depends exclusively on published events.
- Event payloads remain backward compatible.
- All consumers are idempotent.
- Events are published only after successful transaction commits.
- Progress remains the authoritative producer of recognition events.
- Recognition modules never directly modify Learning Workflow state.