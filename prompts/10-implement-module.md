You are implementing one CipherForge module.

Architecture documentation is authoritative.

Read:

- docs
- ADRs
- CodingRules.md

Review neighboring modules before implementation.

Implement ONLY the requested module.

Before coding produce:

1. Responsibilities
2. Public API
3. Dependencies
4. Events Published
5. Events Consumed
6. Database changes
7. Migration plan
8. Files to create
9. Files to modify
10. Risks

Implementation Requirements

- Modular Monolith
- FastAPI
- SQLAlchemy 2.x
- Async
- PostgreSQL
- Redis where required
- Pydantic v2
- Dependency Injection
- Repository Pattern
- Domain Events
- CQRS projections
- Production quality
- Complete type hints

Do not:

- modify unrelated modules
- introduce TODOs
- violate ownership
- bypass services
- access another module's repository

After implementation:

Generate:

Implementation Summary

Architecture Compliance

Known Technical Debt

Tests Added

Documentation Updated

Stop.