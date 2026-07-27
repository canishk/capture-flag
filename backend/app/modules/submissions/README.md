# Submissions Module

## Purpose

Immutable learner attempt records.

## Responsibilities

- Create submission, attempt numbering, history, status tracking, ownership

## Does NOT own

- Evaluation logic, progress, XP, unlocks

## Public API

- `POST /api/v1/submissions`
- `GET /api/v1/submissions/me`
- `GET /api/v1/submissions/challenge/{challengeId}`
- `GET /api/v1/submissions/{submissionId}`
- `GET /api/v1/submissions` (admin)

## Dependencies

- `ChallengeService` — challenge availability validation

## Events

- `SubmissionCreated`, `SubmissionUpdatedStatus`

## Rules

- Answers immutable after creation
- Only status/feedback/processing time updatable (via `SubmissionService.update_submission_status`)
