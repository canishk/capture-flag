# ADR-001: Adopt a Modular Monolith Architecture

- **Status:** Accepted
- **Date:** 2026-07-27
- **Decision Makers:** CipherForge Development Team
- **Type:** Architectural Decision

---

# Context

CipherForge is a Capture The Flag (CTF) learning platform designed to help learners progress through structured cybersecurity challenges.

The platform includes multiple business domains, including:

- Authentication
- Users
- Categories
- Levels
- Challenges
- Hints
- Resources
- Submissions
- Evaluations
- Progress
- Trophies
- Leaderboards
- Notifications
- Analytics
- AI Services

These domains are highly related and will evolve independently over time.

The project is currently developed by a single team and is expected to serve a relatively modest number of users during its initial releases.

Using a microservices architecture at this stage would introduce unnecessary complexity, including:

- Distributed transactions
- Service discovery
- Deployment orchestration
- Increased operational overhead
- Cross-service debugging
- Network latency
- Data synchronization challenges

Conversely, a traditional layered monolith would make it difficult to maintain clear ownership boundaries between business domains as the application grows.

---

# Decision

CipherForge will be implemented as a **Modular Monolith**.

Each business capability is implemented as an independent module with clearly defined responsibilities and ownership.

Modules communicate through:

- Public application services
- Well-defined interfaces
- Domain events

Modules must not directly access another module's repositories or persistence layer.

---

# Module Structure

Every business module should follow a consistent internal structure.

```
module/
│
├── api/
├── application/
├── domain/
├── repositories/
├── infrastructure/
├── schemas/
├── events/
├── tests/
└── README.md
```

Each module owns:

- Domain models
- Persistence
- Business rules
- APIs
- Events
- Tests

---

# Architectural Principles

## High Cohesion

Each module owns a single business capability.

Example:

```
Challenge Module

✓ Challenge CRUD
✓ Publish
✓ Archive
✓ Metadata

✗ Progress
✗ Evaluation
✗ Trophy Logic
```

---

## Loose Coupling

Modules communicate through explicit contracts.

Allowed:

```
Module A

↓

Application Service

↓

Module B
```

or

```
Module A

↓

Domain Event

↓

Module B
```

Not allowed:

```
Module A

↓

Module B Repository
```

---

## Repository Ownership

Repositories belong exclusively to their owning module.

Only the owning module may:

- Create
- Update
- Delete
- Query using internal persistence models

External modules must communicate through published interfaces.

---

## Shared Database

All modules share a single relational database.

However, database ownership remains at the module level.

Sharing a database does **not** imply shared ownership of tables.

Each module owns its own schema objects.

---

## Deployment Model

CipherForge is deployed as a single application.

Advantages include:

- Simple deployment
- Single transaction boundary
- Easier debugging
- Simplified testing
- Lower operational cost

The architecture should remain compatible with future extraction of modules into independent services if required.

---

# Benefits

The Modular Monolith approach provides:

- Clear ownership boundaries
- High maintainability
- Strong encapsulation
- Easier testing
- Simpler deployments
- Lower infrastructure cost
- Reduced operational complexity
- Compatibility with Domain-Driven Design (DDD)

---

# Trade-offs

This architecture also introduces some limitations.

- A single deployable unit
- Shared runtime resources
- Careful enforcement of module boundaries is required
- Team discipline is essential to prevent tight coupling

These trade-offs are acceptable for the expected scale of the project.

---

# Future Evolution

If future requirements demand independent scaling or deployments, individual modules may be extracted into microservices.

Because communication occurs through public interfaces and domain events, such extraction should require minimal changes to business logic.

The current architecture intentionally preserves this migration path.

---

# Alternatives Considered

## Traditional Layered Monolith

Rejected because:

- Weak business boundaries
- Higher risk of tightly coupled code
- Difficult to evolve independently

---

## Microservices

Rejected because:

- Operational complexity
- Distributed transactions
- Infrastructure overhead
- Increased development effort
- Premature optimization for the current project size

---

# Consequences

## Positive

- Clear module ownership
- Strong separation of concerns
- Simplified development
- Easier onboarding
- Easier testing
- Single deployment pipeline
- Natural evolution toward event-driven architecture

## Negative

- Requires architectural discipline
- Shared process means a faulty module can affect the entire application
- Scaling is application-wide rather than per module

---

# Compliance

The architecture complies with this ADR when:

- Every business capability is implemented as an independent module.
- Modules expose only documented public interfaces.
- No module directly accesses another module's repositories.
- Business logic remains within the owning module.
- Domain events are used for asynchronous communication.
- Module boundaries are preserved during future development.

---

# Review

This ADR should be reviewed if:

- The application requires independent deployment of modules.
- Operational scaling requirements significantly increase.
- Team size or organizational structure changes substantially.
- The current modular boundaries no longer support the business domain effectively.