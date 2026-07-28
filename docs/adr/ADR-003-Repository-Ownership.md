# ADR-003: Repository Ownership and Data Access Rules

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

CipherForge follows a Modular Monolith architecture with clearly defined bounded contexts.

Although all modules share the same relational database, unrestricted access to repositories or tables would eventually create:

- Tight coupling
- Hidden dependencies
- Circular references
- Business logic leakage
- Difficult testing
- Fragile refactoring

A shared database must not become a shared ownership model.

Therefore, repository ownership must be explicitly defined.

---

# Decision

Every repository belongs exclusively to a single module.

Only the owning module may directly:

- Create entities
- Update entities
- Delete entities
- Execute repository queries
- Construct ORM models
- Define persistence mappings

All other modules must communicate through:

- Public application services
- Published interfaces
- Domain events

Repository access across module boundaries is prohibited.

---

# Repository Ownership

## Authentication

Owns

- AuthRepository
- TokenRepository

---

## Users

Owns

- UserRepository
- UserPreferenceRepository

---

## Categories

Owns

- CategoryRepository

---

## Levels

Owns

- LevelRepository

---

## Challenges

Owns

- ChallengeRepository

---

## Hints

Owns

- HintRepository

---

## Resources

Owns

- ResourceRepository

---

## Submissions

Owns

- SubmissionRepository

---

## Evaluations

Owns

- EvaluationRepository

---

## Progress

Owns

- ProgressRepository

---

## Recognition

Owns

- TrophyRepository
- AchievementRepository
- LeaderboardRepository
- StreakRepository

---

# Allowed Communication

## Public Application Services

Allowed

```
SubmissionService

↓

ChallengeService
```

The service owns its repository and performs the persistence work internally.

---

## Domain Events

Allowed

```
EvaluationCompleted

↓

Progress Event Handler

↓

ProgressRepository
```

The event handler belongs to the Progress module and therefore may access the ProgressRepository.

---

## Public Read Interfaces

Allowed

```
LeaderboardService

↓

ProgressQueryService
```

The query service exposes only documented read operations.

No repository is shared.

---

# Prohibited Access

The following patterns are architectural violations.

## Cross-Module Repository Injection

Not allowed

```
class SubmissionService:

    def __init__(
        self,
        submission_repo,
        challenge_repo
    ):
        ...
```

The Submission module must not receive a ChallengeRepository.

---

## Direct Repository Import

Not allowed

```
from challenge.repositories import ChallengeRepository
```

Only the Challenge module may import its repository.

---

## Cross-Module ORM Queries

Not allowed

```
session.query(Challenge)
```

inside the Submission module.

The Challenge entity belongs to the Challenge module.

---

## Direct Table Updates

Not allowed

```
UPDATE progress
SET xp = ...
```

from the Evaluation module.

Progress owns its own persistence.

---

# Repository Interfaces

Repositories should expose interfaces rather than concrete implementations.

Example

```
ChallengeRepository
        ▲
        │
SQLAlchemyChallengeRepository
```

Application services depend on abstractions.

Infrastructure provides implementations.

---

# Read vs Write Access

Repositories perform persistence only.

Business rules belong in application/domain services.

Repository responsibilities include:

- CRUD
- Queries
- Persistence mapping
- Transactions delegated by the service

Repositories must not:

- Calculate XP
- Unlock levels
- Evaluate answers
- Award trophies
- Publish events

---

# Query Services

Read-heavy operations that span multiple modules should be implemented using dedicated query services.

Example

```
LeaderboardQueryService

↓

ProgressQueryService

↓

ProgressRepository
```

Rather than allowing LeaderboardRepository to query Progress tables directly.

---

# Shared Database Rules

A shared database does not imply shared ownership.

Each table belongs to one module.

| Table | Owner |
|--------|-------|
| users | Users |
| categories | Categories |
| levels | Levels |
| challenges | Challenges |
| hints | Hints |
| resources | Resources |
| submissions | Submissions |
| evaluations | Evaluations |
| progress | Progress |
| trophies | Recognition |

Ownership determines who may modify the table.

---

# Event-Based Updates

Cross-domain state changes occur through events.

Example

```
Submission

↓

EvaluationCompleted

↓

Progress

↓

ChallengeCompleted

↓

Recognition
```

Repositories never communicate directly.

---

# Testing

Repository tests verify:

- Persistence
- Queries
- Constraints
- Transactions

Business rules must be tested in services, not repositories.

Repository tests should not depend on another module's repositories.

---

# Exceptions

Temporary exceptions may be permitted only when:

- A documented ADR approves the exception.
- There is no reasonable alternative.
- The exception is explicitly marked as technical debt.
- A removal plan exists.

Undocumented exceptions are prohibited.

---

# Consequences

## Positive

- Strong module encapsulation
- Clear ownership
- Easier refactoring
- Better unit testing
- Reduced coupling
- Improved maintainability
- Cleaner dependency graph

## Negative

- More service interfaces
- Slightly more boilerplate
- Cross-module workflows require coordination through services or events

These trade-offs are accepted in exchange for long-term maintainability.

---

# Compliance Checklist

The architecture complies with this ADR when:

- Every repository has exactly one owning module.
- No module imports another module's repository.
- Cross-module communication occurs through services, interfaces, or events.
- Repositories contain persistence logic only.
- Business rules remain outside repositories.
- Repository ownership is enforced during code reviews.

---

# Review

This ADR should be reviewed when:

- A new bounded context is introduced.
- A repository is split or merged.
- The persistence technology changes.
- The application evolves from a modular monolith toward distributed services.