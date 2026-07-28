# ADR-004: Adopt CQRS and Event-Driven Architecture

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

CipherForge supports a learning workflow that progresses through several business domains:

```
Challenge

↓

Submission

↓

Evaluation

↓

Progress

↓

Recognition

↓

Analytics
```

Each stage has different responsibilities.

For example:

- Submissions record immutable learner attempts.
- Evaluations determine correctness.
- Progress represents the learner's current state.
- Recognition awards trophies and achievements.
- Analytics aggregates historical information.

If these responsibilities are implemented using a single mutable domain model, several problems arise:

- Business logic becomes tightly coupled.
- Read models become expensive to compute.
- Multiple modules modify the same data.
- Reporting impacts transactional performance.
- Future asynchronous processing becomes difficult.

CipherForge requires a clear separation between operational workflows and read-optimized views.

---

# Decision

CipherForge adopts **Command Query Responsibility Segregation (CQRS)** combined with **Domain Events**.

This does **not** imply separate databases or microservices.

Instead:

- Commands modify authoritative domain state.
- Queries read optimized projections.
- Domain events communicate state changes between modules.

---

# CQRS Principles

The system distinguishes between:

## Command Model

Responsible for changing state.

Examples:

- Create Submission
- Evaluate Submission
- Publish Challenge
- Update Category
- Create Resource

Command models own business rules.

---

## Query Model

Responsible for reading state.

Examples:

- Learner dashboard
- Progress summary
- Resume learning
- Leaderboards
- Analytics

Query models never change business state.

---

# Write Model

The authoritative write model consists of:

```
Authentication

Users

Categories

Levels

Challenges

Hints

Resources

Submissions

Evaluations
```

These modules own transactional business logic.

---

# Read Model

Read projections include:

```
Progress

Leaderboards

Achievements

Dashboard

Analytics
```

Read models are derived from write models.

They are **never** the source of truth.

---

# Domain Events

Modules communicate through immutable domain events.

Examples:

```
SubmissionCreated

EvaluationCompleted

ProgressUpdated

ChallengeCompleted

LevelCompleted

CategoryCompleted
```

Events describe something that **has already happened**.

They never represent commands.

---

# Event Flow

The canonical learning workflow is:

```
Challenge

↓

Submission

↓

Evaluation

↓

Progress Projection

↓

ChallengeCompleted

↓

Recognition

↓

Analytics
```

No module may bypass this workflow.

---

# Progress as a Projection

The Progress module is a read projection.

It is derived from:

- Submissions
- Evaluations
- Domain Events

Progress must never become a second source of truth.

Examples of data owned by Progress:

- XP totals
- Completed challenges
- Completed levels
- Completed categories
- Resume position
- Completion percentages

Progress does **not** own:

- Answers
- Evaluation logic
- Challenge definitions

---

# Commands

Commands represent requests to change state.

Examples:

```
CreateSubmission

EvaluateSubmission

PublishChallenge

ArchiveChallenge
```

Commands execute synchronously within the owning module.

Commands may publish events after successful completion.

---

# Events

Events represent completed business facts.

Examples:

```
SubmissionCreated

↓

EvaluationCompleted

↓

ProgressUpdated

↓

ChallengeCompleted
```

Events are immutable.

Consumers must treat them as historical records.

---

# Event Publication

Events are published only after a successful transaction commits.

```
Create Submission

↓

Persist Submission

↓

Commit

↓

Publish SubmissionCreated
```

Events must never be published before persistence succeeds.

The architecture is compatible with introducing the **Outbox Pattern** in the future.

---

# Event Consumers

Consumers subscribe to events without creating dependencies on producer repositories.

Example:

```
EvaluationCompleted

↓

Progress
```

Later:

```
ChallengeCompleted

↓

Recognition
```

Then:

```
ProgressUpdated

↓

Analytics
```

Producer modules remain unaware of consumers.

---

# Idempotency

All event consumers must be idempotent.

Processing the same event multiple times must produce the same final state.

Example:

```
ChallengeCompleted

↓

Already Processed?

↓

Yes

↓

Ignore
```

Duplicate events must never produce duplicate trophies, XP, or leaderboard entries.

---

# Event Ordering

Ordering is guaranteed only within a logical aggregate (such as a single learner).

Consumers must not depend on global event ordering.

When ordering matters, use:

- Aggregate identifier
- Event version
- Event timestamp

---

# Event Payloads

Events should contain only the information required by downstream consumers.

Payloads should:

- Be immutable
- Be self-contained
- Avoid sensitive information
- Remain backward compatible

Large object graphs must never be embedded in events.

---

# Transactions

A command owns the transaction.

Typical transaction:

```
Create Submission

↓

Persist Submission

↓

Evaluate Submission

↓

Persist Evaluation

↓

Commit

↓

Publish Events
```

Read projections update after the transaction commits.

---

# Read Projection Rebuild

Every projection should be rebuildable.

The platform should support rebuilding projections from authoritative data or replayed events.

Examples:

- Progress rebuild
- Leaderboard rebuild
- Achievement rebuild

Rebuilding must not modify authoritative write data.

---

# Module Responsibilities

| Module | Role |
|---------|------|
| Submission | Write Model |
| Evaluation | Write Model |
| Progress | Read Projection |
| Recognition | Event Consumer |
| Analytics | Event Consumer |

Ownership remains unchanged.

---

# Alternatives Considered

## Traditional CRUD

Rejected because:

- Read and write responsibilities become tightly coupled.
- Reporting queries impact transactional workloads.
- Projection logic becomes duplicated.

---

## Full Event Sourcing

Rejected because:

- Higher implementation complexity.
- Increased operational overhead.
- Current project requirements do not justify storing events as the sole source of truth.

However, the architecture remains compatible with future evolution toward event sourcing if required.

---

# Consequences

## Positive

- Clear separation of reads and writes.
- Independent evolution of projections.
- Loose coupling between modules.
- Improved scalability for reporting.
- Easier addition of Recognition and Analytics.
- Compatible with asynchronous processing.
- Simplifies future microservice extraction.

## Negative

- Eventual consistency between write and read models.
- Additional event handling infrastructure.
- Projection rebuild mechanisms must be maintained.
- More architectural discipline is required.

---

# Compliance Checklist

The architecture complies with this ADR when:

- Commands modify only their owning domain.
- Queries never modify business state.
- Progress remains a projection.
- Domain events are immutable.
- Events are published only after successful commits.
- Consumers are idempotent.
- Cross-module communication uses services or domain events.
- No module bypasses the canonical learning workflow.

---

# Review

This ADR should be reviewed when:

- Additional projections are introduced.
- Event contracts change.
- Asynchronous messaging infrastructure is added.
- The application adopts the Outbox Pattern or distributed event brokers.
- The architecture evolves toward event sourcing or microservices.