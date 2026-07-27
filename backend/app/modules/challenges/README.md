# Challenges Module

## Purpose

Core learning activity — challenge metadata, lifecycle, scoring/evaluation configuration.

## Responsibilities

- Challenge CRUD, publish, hide, archive, reorder
- Metadata, objectives, difficulty, visibility
- Category/Level associations via public services

## Does NOT own

- Hints, Resources, Submissions, Evaluations, Progress

## Public API

- `GET /api/v1/challenges`
- `GET /api/v1/challenges/{challengeId}`
- `POST /api/v1/challenges` (admin)
- `PATCH /api/v1/challenges/{challengeId}` (admin)
- `DELETE /api/v1/challenges/{challengeId}` (admin hide)
- `POST /api/v1/challenges/{challengeId}/publish` (admin)
- `POST /api/v1/challenges/{challengeId}/archive` (admin)
- `PATCH /api/v1/challenges/{challengeId}/order` (admin)

## Dependencies

- `CategoryService`, `LevelService` — placement validation only

## Events

- `ChallengeCreated`, `ChallengeUpdated`, `ChallengePublished`, `ChallengeHidden`, `ChallengeArchived`
