# ADR-002: Establish Domain Boundaries and Module Ownership

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

CipherForge consists of multiple business capabilities that evolve independently.

Without explicit domain boundaries, business logic can become tightly coupled, resulting in:

- God services
- Cross-module dependencies
- Circular references
- Shared business rules
- Difficult testing
- Poor maintainability

To preserve a modular architecture, every business capability must have a clearly defined owner and explicit responsibilities.

---

# Decision

CipherForge adopts **Domain-Driven Design (DDD)** inspired bounded contexts.

Each business capability is implemented as an independent module with:

- its own domain model
- its own business rules
- its own persistence
- its own APIs
- its own events

Every module is the **single source of truth** for its own domain.

No other module may implement or duplicate its business rules.

---

# Domain Map

```
Identity

├── Authentication
└── Users

        │

        ▼

Learning Content

├── Categories
├── Levels
├── Challenges
├── Hints
└── Resources

        │

        ▼

Learning Workflow

├── Submissions
├── Evaluations
└── Progress

        │

        ▼

Recognition

├── Trophies
├── Achievements
├── Leaderboards
└── Streaks

        │

        ▼

Platform

├── Notifications
├── Analytics
├── AI
└── Administration
```

Dependencies always flow downward.

---

# Domain Responsibilities

## Authentication

Owns:

- Login
- Logout
- JWT
- Password hashing
- Password reset
- Email verification
- Authentication tokens

Does not own:

- User profile
- Learning progress
- Authorization decisions outside authentication

---

## Users

Owns:

- User profile
- Avatar
- Preferences
- Display name
- Public profile

Does not own:

- Authentication
- Passwords
- Progress
- Achievements

---

## Categories

Owns:

- Category lifecycle
- Ordering
- Visibility
- Publication

Does not own:

- Levels
- Challenges
- Progress

---

## Levels

Owns:

- Level lifecycle
- Unlock sequence
- Ordering

Does not own:

- Challenges
- Progress

---

## Challenges

Owns:

- Challenge definition
- Metadata
- Difficulty
- Objectives
- Publication

Does not own:

- Hints
- Resources
- Submissions
- Evaluation
- Progress

---

## Hints

Owns:

- Hint content
- Unlock sequence
- Penalties
- Visibility

Does not own:

- Challenge logic
- Evaluation

---

## Resources

Owns:

- Learning materials
- External links
- Reusable content
- Resource metadata

Does not own:

- Challenge completion
- Progress

---

## Submissions

Owns:

- Learner attempts
- Submitted answers
- Submission history
- Submission status

Rules:

- Immutable answers
- New attempt creates a new submission

Does not own:

- Evaluation
- XP
- Progress
- Unlocks

---

## Evaluations

Owns:

- Answer evaluation
- Scoring
- Pass/fail decisions
- Feedback
- Evaluation strategy selection

Does not own:

- Submission persistence
- Progress
- Recognition

---

## Progress

Owns:

- Progress projection
- XP totals
- Completion percentages
- Resume state
- Completion events

Progress is **not** the source of truth.

It derives its state from:

- Submissions
- Evaluations
- Domain events

Does not own:

- Evaluation rules
- Submissions
- Challenge data

---

## Recognition

Owns:

- Trophies
- Achievements
- Leaderboards
- Streaks

Consumes events from Progress.

Does not modify Learning Workflow state.

---

## Notifications

Owns:

- User notifications
- Delivery channels
- Notification preferences

Consumes domain events.

Never implements business rules owned by other domains.

---

## Analytics

Owns:

- Aggregated reporting
- Metrics
- Dashboards
- Historical trends

Consumes events.

Never modifies operational data.

---

## AI

Owns:

- AI evaluation strategies
- Recommendations
- Learning assistance
- Hint generation

Does not own:

- Progress
- Recognition
- Challenge lifecycle

---

# Dependency Rules

Dependencies may only point toward lower-level shared capabilities or published contracts.

Allowed:

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
```

Not allowed:

```
Progress

↓

Submission Repository
```

or

```
Recognition

↓

Evaluation Repository
```

---

# Communication Rules

Modules communicate through one of the following:

## Application Services

For synchronous requests.

Example:

```
ChallengeService

↓

CategoryService
```

---

## Domain Events

For asynchronous communication.

Example:

```
EvaluationCompleted

↓

Progress

↓

ChallengeCompleted

↓

Recognition
```

---

## Public Interfaces

When shared functionality is required.

Modules must not expose internal implementation details.

---

# Source of Truth

Each business concept has exactly one owner.

| Concept | Owner |
|----------|-------|
| User | Users |
| Password | Authentication |
| Challenge | Challenges |
| Hint | Hints |
| Resource | Resources |
| Submission | Submissions |
| Evaluation | Evaluations |
| Progress | Progress |
| Trophy | Recognition |

No duplicate ownership is permitted.

---

# Boundary Violations

The following are architectural violations:

- Cross-module repository access
- Business logic copied between modules
- Circular dependencies
- Hidden ownership
- Shared mutable state
- Direct database access into another module's tables

Such violations must be corrected before merging.

---

# Future Evolution

New bounded contexts should follow the same principles.

Potential future modules include:

- Organizations
- Teams
- Competitions
- Certificates
- Marketplace
- Learning Paths

Each must define:

- ownership
- responsibilities
- public interfaces
- events

before implementation begins.

---

# Alternatives Considered

## Layer-Based Architecture

Rejected because business rules become scattered across controllers, services, and repositories without clear ownership.

## Shared Domain Model

Rejected because multiple modules would become responsible for the same business concepts, leading to ambiguity and tight coupling.

---

# Consequences

## Positive

- Clear ownership of business logic
- Independent module evolution
- Improved maintainability
- Easier testing
- Reduced coupling
- Better scalability of the codebase
- Consistent architectural reviews

## Negative

- Requires discipline to maintain boundaries
- Some workflows require event-based coordination
- Additional interfaces and contracts must be maintained

---

# Compliance

The architecture complies with this ADR when:

- Every business concept has a single owning module.
- Modules implement only their assigned responsibilities.
- Cross-module communication occurs through services, interfaces, or domain events.
- No module directly accesses another module's repositories or persistence layer.
- Architectural reviews enforce these boundaries before code is merged.

---

# Review

This ADR should be revisited when:

- New bounded contexts are introduced.
- Existing domains are split or merged.
- The application transitions from a modular monolith to distributed services.
- Significant business capabilities require re-evaluating ownership boundaries.