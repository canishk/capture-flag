# Sprint 4 – Recognition Domain

## Goal

Implement the Recognition bounded context as an independent event consumer.

Recognition must never access Learning Workflow repositories directly.

It consumes only published domain events.

## Modules

1. Trophies
2. Achievements
3. Leaderboards
4. Integration
5. Recognition Domain Review
6. Sprint Review

## Implementation Order

```
Trophies

↓

Review

↓

Achievements

↓

Review

↓

Leaderboards

↓

Review

↓

Integration

↓

Recognition Review

↓

Sprint Review
```

## Required Reading

Read before implementation:

- docs/adr/ADR-001-Modular-Monolith.md
- docs/adr/ADR-002-Domain-Boundaries.md
- docs/adr/ADR-003-Repository-Ownership.md
- docs/adr/ADR-004-CQRS-and-Event-Driven-Architecture.md
- docs/adr/ADR-005-Recognition-Event-Contracts.md
- docs/adr/ADR-006-Recognition-Engine-Architecture.md
- docs/adr/ADR-007-Domain-Event-Processing-and-Reliability.md

Do not begin coding until these ADRs have been reviewed.