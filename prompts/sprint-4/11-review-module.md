# Module Architecture Review

Review the implementation of the current Sprint 4 module before proceeding to the next module.

Do **not** implement new functionality.

Your objective is to verify that the implementation complies with the project's architecture, ADRs, and coding standards.

---

## Required Reading

Review the following before beginning:

- docs/adr/ADR-001-Modular-Monolith.md
- docs/adr/ADR-002-Domain-Boundaries.md
- docs/adr/ADR-003-Repository-Ownership.md
- docs/adr/ADR-004-CQRS-and-Event-Driven-Architecture.md
- docs/adr/ADR-005-Recognition-Event-Contracts.md
- docs/adr/ADR-006-Recognition-Engine-Architecture.md
- docs/adr/ADR-007-Domain-Event-Processing-and-Reliability.md

---

# Review Areas

## 1. Domain Boundaries

Verify that the module owns only its assigned business responsibilities.

Ensure:

- No business logic belongs to another module.
- No duplicated business rules.
- No hidden ownership.
- Single responsibility is maintained.

---

## 2. Repository Ownership

Verify:

- Only this module accesses its repositories.
- No repositories from another bounded context are imported.
- No direct SQL against another module's tables.
- Repository responsibilities remain persistence-only.

Flag any boundary violations.

---

## 3. CQRS Compliance

Verify:

- Commands modify only this module's state.
- Queries do not modify data.
- Read models remain projections.
- No command/query mixing.

---

## 4. Event-Driven Architecture

Verify:

- Correct event subscriptions.
- Events are published only after successful persistence.
- Consumers are idempotent.
- Events are immutable.
- Event payloads comply with ADR-005.
- No synchronous coupling to producer modules.

---

## 5. Recognition Engine Compliance

If applicable, verify:

- Recognition Engine performs orchestration only.
- Business rules remain inside module services.
- Event routing is centralized.
- No orchestration logic exists in controllers or repositories.

---

## 6. Service Layer

Review:

- Service responsibilities
- Business rule placement
- Dependency injection
- Transaction boundaries
- Error handling
- Separation of concerns

Ensure services are cohesive and do not become "God Services."

---

## 7. API Layer

Verify:

- REST endpoints follow project conventions.
- Validation is implemented.
- Authorization is enforced where required.
- HTTP status codes are appropriate.
- API does not expose internal implementation details.

---

## 8. Domain Model

Review:

- Entity design
- Value objects
- Enumerations
- Aggregates
- Invariants

Ensure domain logic resides in the domain or application layer—not repositories.

---

## 9. Database

Verify:

- Proper indexes
- Constraints
- Foreign keys
- Cascade rules
- Migration quality

Check for unnecessary database coupling.

---

## 10. Security

Review:

- Authorization
- Input validation
- Event validation
- Data exposure
- Sensitive information leakage

Ensure event payloads expose only the minimum required information.

---

## 11. Performance

Review:

- Database queries
- Event processing
- Projection updates
- N+1 query issues
- Repository efficiency

Recommend improvements where appropriate.

---

## 12. Testing

Review:

- Unit tests
- Integration tests
- Event handling tests
- Idempotency tests
- Edge cases
- Failure scenarios

Ensure new functionality is adequately covered.

---

## 13. Documentation

Verify:

- Module README
- API documentation
- Architecture documentation
- Event documentation
- Inline code comments where appropriate

---

# Technical Debt

Categorize findings as:

## Critical

Must be fixed before continuing.

## High

Should be fixed before the end of the sprint.

## Medium

Can be scheduled for a future sprint.

## Low

Minor improvements or cleanup.

---

# Deliverables

Produce a review report containing:

## Executive Summary

A brief assessment of the module's overall quality and readiness.

## Architecture Score

Score out of 10.

## Security Score

Score out of 10.

## Maintainability Score

Score out of 10.

## Test Coverage Assessment

Summarize the quality and completeness of testing.

## Findings

Organize issues by:

- Critical
- High
- Medium
- Low

## Recommendations

Provide actionable recommendations to improve the module.

## Sprint Readiness

Conclude with exactly one of:

- ✅ Ready to proceed to the next module.
- ⚠️ Proceed with minor improvements.
- ❌ Blocked until critical issues are resolved.

Do not modify code.

Produce only the review report.