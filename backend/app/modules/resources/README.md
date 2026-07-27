# Resources Module

## Purpose

Reusable learning assets — independent bounded context with M2M challenge association.

## Responsibilities

- Resource CRUD, types, visibility, challenge linking

## Does NOT own

- Challenge logic, progress, evaluations

## Public API

- `GET /api/v1/resources`
- `GET /api/v1/resources/{resourceId}`
- `GET /api/v1/resources/challenge/{challengeId}`
- `POST /api/v1/resources` (admin)
- `PATCH /api/v1/resources/{resourceId}` (admin)
- `DELETE /api/v1/resources/{resourceId}` (admin hide)
- `POST /api/v1/resources/{resourceId}/publish` (admin)
- `POST /api/v1/resources/{resourceId}/link` (admin)
- `POST /api/v1/resources/{resourceId}/unlink` (admin)

## Dependencies

- `ChallengeService` — challenge existence validation for linking only

## Events

- `ResourceCreated`, `ResourceUpdated`, `ResourcePublished`, `ResourceHidden`, `ResourceLinked`
