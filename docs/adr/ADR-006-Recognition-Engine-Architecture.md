# ADR-006: Recognition Engine Architecture

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

Sprint 4 introduces the Recognition bounded context.

Recognition is responsible for rewarding learners based on their learning activity without coupling itself to the Learning Workflow.

The Recognition domain currently consists of:

- Trophies
- Achievements
- Leaderboards

Future capabilities include:

- Streaks
- Certificates
- Activity Feed
- Reputation
- AI Coaching Rewards

Each capability responds to events produced by the Learning Workflow.

Without a common architecture, each feature would independently subscribe to events, implement its own rules, and duplicate logic for:

- Event handling
- Rule evaluation
- Award tracking
- Idempotency
- Progress calculations

This would increase maintenance cost and make adding new recognition features progressively harder.

---

# Decision

CipherForge adopts a **Recognition Engine** architecture.

The Recognition Engine acts as the orchestration layer inside the Recognition bounded context.

Its responsibilities are:

- Receive Recognition-related domain events.
- Dispatch events to registered recognition modules.
- Execute recognition rules.
- Persist recognition state.
- Publish recognition events.

The Recognition Engine does **not** own learning workflow data.

---

# Architecture

```
Progress

↓

ChallengeCompleted
LevelCompleted
CategoryCompleted
ProgressUpdated

↓

Recognition Engine

├── Trophy Engine
├── Achievement Engine
├── Leaderboard Engine
└── Future Engines

↓

Recognition Events
```

The Learning Workflow remains completely unaware of the Recognition Engine.

---

# Recognition Components

## Recognition Engine

Responsibilities:

- Event routing
- Rule orchestration
- Idempotency enforcement
- Shared transaction boundaries
- Common logging
- Metrics
- Error handling

The engine contains no recognition-specific business rules.

---

## Trophy Engine

Responsible for:

- Trophy definitions
- Trophy eligibility
- Trophy awards
- Trophy history

Consumes:

- ChallengeCompleted
- LevelCompleted
- CategoryCompleted

Publishes:

- TrophyAwarded

---

## Achievement Engine

Responsible for:

- Achievement definitions
- Multi-stage progress
- Hidden achievements
- Badge metadata

Consumes:

- ChallengeCompleted
- ProgressUpdated
- TrophyAwarded

Publishes:

- AchievementUnlocked

---

## Leaderboard Engine

Responsible for:

- XP rankings
- Weekly rankings
- Monthly rankings
- All-time rankings
- Category rankings

Consumes:

- ProgressUpdated

Publishes:

- LeaderboardUpdated (optional)

---

# Rule Isolation

Each recognition module owns its own rules.

Example:

```
ChallengeCompleted

↓

Recognition Engine

↓

Trophy Engine

↓

Award "First Challenge"
```

The Achievement Engine does not know how trophies are calculated.

Likewise, the Trophy Engine does not know how leaderboards are updated.

---

# Event Processing

The Recognition Engine receives events from the Learning Workflow.

Example:

```
ChallengeCompleted

↓

Recognition Engine

↓

Trophy Engine

↓

Achievement Engine

↓

Publish TrophyAwarded
```

Each module processes the event independently.

Failures in one module must not prevent others from completing.

---

# Idempotency

Every recognition module must guarantee idempotent processing.

Example:

```
ChallengeCompleted

↓

Already processed?

↓

Yes

↓

Ignore
```

Duplicate events must never produce:

- Duplicate trophies
- Duplicate achievements
- Duplicate leaderboard entries

---

# Repository Ownership

Each recognition module owns its own persistence.

| Repository | Owner |
|------------|-------|
| TrophyRepository | Trophy Engine |
| AchievementRepository | Achievement Engine |
| LeaderboardRepository | Leaderboard Engine |

Modules must never access repositories owned by:

- Progress
- Evaluation
- Submission
- Challenges

Recognition consumes events only.

---

# Recognition Events

Recognition may publish new domain events.

Examples:

```
TrophyAwarded

AchievementUnlocked

LeaderboardUpdated

StreakCompleted

CertificateEarned
```

These events enable future integrations without changing Recognition internals.

---

# Transaction Boundaries

Each incoming event is processed independently.

```
Receive Event

↓

Recognition Engine

↓

Recognition Module

↓

Commit

↓

Publish Recognition Event
```

A failure in one recognition module must not roll back the originating Learning Workflow transaction.

---

# Extensibility

New recognition capabilities are added by registering new engines.

Example:

```
Recognition Engine

├── Trophy Engine
├── Achievement Engine
├── Leaderboard Engine
├── Streak Engine
├── Certificate Engine
└── Reputation Engine
```

Existing modules remain unchanged.

This follows the **Open/Closed Principle**.

---

# Dependency Rules

Allowed:

```
Progress

↓

Recognition Engine

↓

Recognition Modules
```

Not Allowed:

```
Recognition

↓

Progress Repository
```

or

```
Recognition

↓

Evaluation Repository
```

Recognition depends only on published event contracts.

---

# Alternatives Considered

## Independent Event Subscribers

Rejected because each recognition feature would duplicate:

- Event subscriptions
- Error handling
- Idempotency
- Logging
- Monitoring

---

## Single Recognition Service

Rejected because all recognition rules would accumulate in one service, leading to a "God Service" that becomes difficult to maintain.

---

# Consequences

## Positive

- Clear separation of recognition responsibilities.
- Centralized event orchestration.
- Reusable infrastructure for future recognition features.
- Independent evolution of trophies, achievements, and leaderboards.
- Simplified testing.
- Supports future asynchronous processing.
- Compatible with the Outbox Pattern and message brokers.

## Trade-offs

- Introduces an orchestration layer.
- Requires standardized event contracts.
- Slight increase in implementation complexity.

These trade-offs are accepted to maintain long-term modularity and extensibility.

---

# Compliance Checklist

The architecture complies with this ADR when:

- Recognition consumes only published domain events.
- Every recognition capability owns its own repository.
- Recognition modules are independent.
- The Recognition Engine contains orchestration logic only.
- Recognition modules do not access Learning Workflow repositories.
- Recognition events are published after successful processing.
- Consumers implement idempotent event handling.

---

# Review

This ADR should be reviewed when:

- New recognition capabilities are introduced.
- Recognition is distributed into separate services.
- Event processing infrastructure changes.
- A rule engine or workflow engine replaces the current orchestration model.
- The application evolves from in-process events to asynchronous messaging.