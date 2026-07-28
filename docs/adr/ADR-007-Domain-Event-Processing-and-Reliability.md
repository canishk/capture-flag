# ADR-007: Domain Event Processing and Reliability

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

CipherForge uses Domain Events to communicate between bounded contexts.

The current implementation uses **in-process event publication** within the modular monolith.

As the platform grows, additional consumers will subscribe to these events:

- Recognition
- Notifications
- Analytics
- AI Coach
- Activity Feed
- Recommendation Engine

A failure in one consumer must never compromise the transactional integrity of the Learning Workflow.

Furthermore, the architecture should support a future migration to asynchronous messaging (for example, RabbitMQ, Kafka, or AWS EventBridge) without requiring changes to domain logic.

---

# Decision

CipherForge adopts a **reliable event processing model** based on the following principles:

- Events are published only after successful transaction commits.
- Event consumers are independent.
- Consumers are idempotent.
- Consumer failures are isolated.
- Event contracts remain transport-agnostic.
- The architecture remains compatible with the Outbox Pattern.

This ADR defines how events are processed—not what events exist (covered by ADR-005).

---

# Event Processing Lifecycle

Every domain event follows the same lifecycle.

```
Command

↓

Business Validation

↓

Persist State

↓

Commit Transaction

↓

Publish Domain Event

↓

Dispatch to Consumers

↓

Consumer Processing

↓

Optional Consumer Events
```

No consumer participates in the originating transaction.

---

# Transaction Ownership

The originating module owns the transaction.

Example:

```
Create Submission

↓

Submission

↓

Evaluate Submission

↓

Persist Evaluation

↓

Update Progress

↓

Commit

↓

Publish ChallengeCompleted
```

Once committed, the originating transaction is complete.

Consumers execute separately.

---

# Consumer Independence

Every consumer executes independently.

Example:

```
ChallengeCompleted

├── Trophy Engine
├── Achievement Engine
├── Leaderboard Engine
├── Analytics
└── Notification Service
```

A failure in one consumer must never prevent the others from processing the event.

---

# Failure Isolation

Consumer failures do not roll back producer transactions.

If a consumer fails:

1. Log the error.
2. Mark the event processing attempt as failed.
3. Retry according to platform policy.
4. Escalate persistent failures to operational monitoring.
5. Continue processing unaffected consumers.

Future versions may introduce a Dead Letter Queue (DLQ).

---

# Idempotency

Every consumer must be idempotent.

Consumers should maintain a record of processed event identifiers.

```
Receive Event

↓

event_id exists?

├── Yes → Ignore
└── No  → Process
```

Repeated delivery of the same event must never create duplicate:

- XP
- Trophies
- Achievements
- Notifications
- Leaderboard entries

---

# Event Ordering

Ordering is guaranteed only within a single aggregate.

Example:

```
User A

ChallengeCompleted #1

↓

ChallengeCompleted #2
```

Ordering is **not** guaranteed across different users or aggregates.

Consumers must use:

- Aggregate identifier
- Event version
- Timestamp

when ordering is important.

---

# Event Contracts

Consumers depend only on published event contracts.

They must never rely on:

- Internal services
- Repository implementations
- ORM entities
- Database schemas
- Private APIs

Only the event payload is considered public.

---

# Event Dispatch

The current implementation uses synchronous, in-process dispatch.

```
Publish Event

↓

Event Dispatcher

↓

Registered Consumers
```

The dispatcher is an infrastructure concern.

Domain modules remain unaware of the dispatch mechanism.

---

# Future Outbox Pattern

The event publication mechanism must be replaceable with the Outbox Pattern without changing business logic.

Future architecture:

```
Business Transaction

↓

Persist Domain Data

↓

Persist Outbox Record

↓

Commit

↓

Outbox Publisher

↓

Message Broker

↓

Consumers
```

Domain services must not require modification when this evolution occurs.

---

# Event Broker Compatibility

The event model must remain compatible with external messaging platforms.

Examples include:

- RabbitMQ
- Apache Kafka
- AWS EventBridge
- Azure Service Bus
- Google Pub/Sub

Infrastructure adapters are responsible for transport-specific concerns.

Domain events remain transport-independent.

---

# Retry Policy

Transient failures should be retried.

Typical retry sequence:

```
Attempt 1

↓

Attempt 2

↓

Attempt 3

↓

Dead Letter (future)
```

Retry logic belongs to infrastructure, not domain services.

---

# Observability

Every published event should be traceable.

Recommended metadata:

- event_id
- correlation_id
- causation_id
- producer
- occurred_at
- event_version

Infrastructure should provide:

- Processing metrics
- Failure counts
- Retry counts
- Processing duration
- Consumer success rates

---

# Security

Event payloads must not expose:

- Passwords
- Authentication tokens
- Hidden challenge answers
- Evaluation algorithms
- Internal administrative data
- Personally sensitive information beyond what consumers require

Consumers receive only the minimum data necessary.

---

# Module Responsibilities

| Component | Responsibility |
|-----------|----------------|
| Domain Module | Publish events |
| Event Dispatcher | Route events |
| Consumer | Process events |
| Infrastructure | Retry, logging, monitoring |
| Future Outbox | Reliable delivery |

Each responsibility belongs to one architectural layer.

---

# Alternatives Considered

## Direct Service Calls

Rejected because:

- Tight coupling
- Synchronous dependencies
- Difficult future scaling
- Harder to add new consumers

---

## Shared Repository Access

Rejected because it violates:

- ADR-002 (Domain Boundaries)
- ADR-003 (Repository Ownership)

Consumers should react to events, not query producer persistence directly.

---

## Immediate Adoption of External Message Broker

Rejected because:

- The current modular monolith does not require distributed messaging.
- It would introduce unnecessary operational complexity.

The architecture remains ready for this transition in the future.

---

# Consequences

## Positive

- Reliable event processing.
- Loose coupling.
- Independent consumer evolution.
- Failure isolation.
- Improved observability.
- Compatible with Outbox Pattern.
- Ready for future distributed messaging.

## Trade-offs

- Eventual consistency.
- Additional infrastructure responsibilities.
- Retry management.
- Operational monitoring requirements.

These trade-offs are accepted to improve long-term scalability and resilience.

---

# Compliance Checklist

The architecture complies with this ADR when:

- Events are published only after successful commits.
- Consumers are independent.
- Consumers are idempotent.
- Producer transactions are never rolled back by consumer failures.
- Event contracts remain transport-independent.
- Infrastructure manages retries and observability.
- Domain modules remain unaware of the event dispatch implementation.

---

# Review

This ADR should be reviewed when:

- The Outbox Pattern is introduced.
- External messaging infrastructure is adopted.
- Distributed services are introduced.
- Event delivery guarantees change.
- New operational reliability requirements emerge.