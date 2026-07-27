# Event Model

Version: 1.0

Status: Living Document

Related Documents

- docs/architecture/Overview.md
- docs/architecture/Backend.md
- docs/architecture/DataModel.md
- docs/architecture/API.md
- docs/architecture/ModuleStandards.md

---

# Purpose

This document defines how modules communicate through domain events.

The Event Model promotes loose coupling by allowing modules to react to business events without creating direct dependencies between them.

Events describe **something that has already happened**.

Examples:

- User Registered
- Challenge Started
- Challenge Completed
- Trophy Awarded

Modules should react to events rather than calling each other whenever practical.

---

# Design Principles

The Event Model follows these principles:

- Domain events represent completed business actions.
- Events are immutable.
- Events describe facts, not commands.
- Publishers do not know who consumes an event.
- Multiple modules may subscribe to the same event.
- Event processing should be idempotent whenever possible.

---

# Architecture

```
Module

↓

Business Operation

↓

Domain Event

↓

Event Dispatcher

↓

Subscribers
```

Example:

```
Challenge Module

↓

Challenge Completed

↓

Dispatcher

↓

Progress

Leaderboard

Trophies

Analytics

Notifications
```

---

# Event Categories

CipherForge uses four categories of events.

## User Events

Examples:

- UserRegistered
- UserProfileUpdated
- UserDisabled
- UserEnabled

---

## Learning Events

Examples:

- CategoryViewed
- LevelUnlocked
- ChallengeStarted
- ChallengeCompleted
- HintViewed
- ResourceOpened

---

## Evaluation Events

Examples:

- SubmissionCreated
- SubmissionEvaluated
- EvaluationSucceeded
- EvaluationFailed

---

## Administrative Events

Examples:

- CategoryCreated
- LevelPublished
- ChallengePublished
- ChallengeArchived

---

# Event Structure

Every event contains:

```
eventId

eventType

occurredAt

publisher

aggregateId

aggregateType

payload

metadata
```

---

## Event ID

Globally unique identifier.

Recommended:

UUID v7

---

## Event Type

Examples:

```
ChallengeCompleted

UserRegistered

LevelUnlocked
```

---

## Aggregate

The business object responsible for the event.

Examples:

```
User

Challenge

Level

Submission
```

---

## Payload

Contains business information required by subscribers.

Example:

```
ChallengeCompleted

userId

challengeId

levelId

categoryId

score

completedAt
```

Payloads should contain only information required by consumers.

---

## Metadata

Optional information such as:

- Correlation ID
- Request ID
- Client IP
- User Agent
- API Version

Metadata should never contain secrets.

---

# Event Publishing

Only the owning module may publish events for its aggregate.

Examples:

Users module

Publishes:

- UserRegistered
- UserUpdated

Authentication module

Publishes:

- UserLoggedIn
- PasswordChanged

Challenges module

Publishes:

- ChallengeStarted

Evaluations module

Publishes:

- SubmissionEvaluated

Progress module

Publishes:

- LevelCompleted

Ownership prevents duplicate or conflicting events.

---

# Event Consumption

Modules subscribe only to events they need.

Example

```
ChallengeCompleted

↓

Progress

updates completion
```

```
ChallengeCompleted

↓

Leaderboard

updates score
```

```
ChallengeCompleted

↓

Analytics

records metrics
```

Each subscriber operates independently.

---

# Synchronous vs Asynchronous Events

## Synchronous

Used when immediate consistency is required.

Examples:

- Authorization checks
- Validation
- Transaction completion

---

## Asynchronous

Used when eventual consistency is acceptable.

Examples:

- Notifications
- Analytics
- Trophy calculation
- Recommendation generation

---

# Event Ordering

Ordering is guaranteed only within a single aggregate.

Example:

```
ChallengeStarted

↓

SubmissionCreated

↓

SubmissionEvaluated

↓

ChallengeCompleted
```

Cross-aggregate ordering should never be assumed.

---

# Event Versioning

Events are contracts.

Breaking changes require a new version.

Example:

```
ChallengeCompleted v1

ChallengeCompleted v2
```

Consumers should support version migration where practical.

---

# Event Naming

Past tense.

Correct:

```
ChallengeCompleted

UserRegistered

HintViewed
```

Incorrect:

```
CompleteChallenge

RegisterUser

UpdateScore
```

Commands are not events.

---

# Event Lifecycle

```
Business Operation

↓

Validation

↓

Database Commit

↓

Publish Event

↓

Subscribers Execute
```

Events should only be published after the business transaction has successfully committed.

---

# Retry Policy

Subscribers should:

- Retry transient failures.
- Ignore duplicate events.
- Log permanent failures.
- Avoid infinite retry loops.

---

# Idempotency

Subscribers must safely process duplicate events.

Example:

Receiving the same

```
ChallengeCompleted
```

twice must not award two trophies.

---

# Failure Handling

Subscriber failures must not invalidate the original business transaction.

Example:

Challenge completion succeeds even if:

- Email notification fails.
- Analytics service is unavailable.

---

# Security

Events must never expose:

- Passwords
- Password hashes
- JWT tokens
- Secrets
- API keys

Personally identifiable information should be minimized.

---

# Audit

Important business events should also generate audit records.

Examples:

- UserDisabled
- ChallengePublished
- AdministratorRoleChanged

Audit logs are independent of domain events.

---

# Domain Event Catalogue

## Authentication

Publishes

```
UserRegistered

UserLoggedIn

UserLoggedOut

PasswordChanged

PasswordResetRequested

EmailVerified
```

---

## Users

Publishes

```
UserProfileUpdated

UserDisabled

UserEnabled
```

---

## Categories

Publishes

```
CategoryCreated

CategoryUpdated

CategoryHidden
```

---

## Levels

Publishes

```
LevelCreated

LevelUnlocked

LevelCompleted
```

---

## Challenges

Publishes

```
ChallengeCreated

ChallengePublished

ChallengeStarted

ChallengeArchived
```

---

## Evaluations

Publishes

```
SubmissionCreated

SubmissionEvaluated

EvaluationPassed

EvaluationFailed
```

---

## Progress

Publishes

```
ProgressUpdated

CategoryCompleted

LearningPathCompleted
```

---

## Trophies

Publishes

```
TrophyAwarded
```

---

## Leaderboard

Publishes

```
LeaderboardUpdated
```

---

## Notifications

Publishes

```
NotificationSent
```

---

# Recommended Subscribers

| Event | Subscribers |
|--------|-------------|
| UserRegistered | Analytics, Notifications |
| ChallengeStarted | Analytics |
| SubmissionEvaluated | Progress |
| ChallengeCompleted | Progress, Leaderboard, Trophies, Analytics |
| LevelCompleted | Trophies, Notifications |
| TrophyAwarded | Notifications, Analytics |
| CategoryCompleted | Leaderboard, Analytics |
| UserDisabled | Authentication, Notifications |

---

# Implementation Strategy

Version 1

- In-process event dispatcher
- Python event classes
- Transactional publishing
- Synchronous dispatch where required
- Background worker for asynchronous subscribers

Future versions

- RabbitMQ
- Kafka
- Azure Service Bus
- Google Pub/Sub
- AWS EventBridge

The business event contracts should remain unchanged.

---

# Non-Functional Requirements

- Event dispatch should be reliable.
- Duplicate processing must be safe.
- Failed subscribers must not corrupt business data.
- Events should be observable through structured logging.
- Long-running subscribers should execute asynchronously.

---

# Future Enhancements

Potential additions:

- Event replay
- Event sourcing (selected aggregates)
- Distributed tracing
- Dead-letter queues
- Event schema registry
- Cross-service event streaming

These enhancements should build upon the existing event contracts without changing their semantics.

---

# Guiding Principle

Events answer the question:

**"What business fact has just occurred?"**

Modules should communicate through these business facts rather than direct dependencies, allowing CipherForge to remain modular today and evolve into a distributed architecture in the future without changing its core domain model.