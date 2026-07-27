# Hints Module

## Purpose

Progressive guidance for challenges — independent bounded context.

## Responsibilities

- Hint CRUD, ordering, penalties, unlock rules, visibility

## Does NOT own

- Challenge content, progress, scoring execution

## Public API

- `GET /api/v1/hints/challenge/{challengeId}`
- `GET /api/v1/hints/{hintId}`
- `POST /api/v1/hints` (admin)
- `PATCH /api/v1/hints/{hintId}` (admin)
- `DELETE /api/v1/hints/{hintId}` (admin hide)
- `POST /api/v1/hints/{hintId}/publish` (admin)
- `PATCH /api/v1/hints/challenge/{challengeId}/order` (admin)

## Dependencies

- `ChallengeService` — challenge existence validation only

## Events

- `HintCreated`, `HintUpdated`, `HintPublished`, `HintHidden`
