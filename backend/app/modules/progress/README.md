# Progress Module

## Purpose

Event-driven read projection of learner state.

## Responsibilities

- Challenge/level/category completion, XP, statistics, resume state

## Does NOT own

- Submissions, evaluations, answer validation

## Public API

- `GET /api/v1/progress/me`
- `GET /api/v1/progress/summary`

## Dependencies

- `ChallengeService`, `LevelService` — completion checks only

## Events Consumed

- `SubmissionCreated`, `EvaluationCompleted`

## Events Published

- `ProgressUpdated`, `ChallengeCompleted`, `LevelCompleted`, `CategoryCompleted`

## Rules

- Projection only — not source of truth
- Idempotent completion recording
- Duplicate pass events → no double XP
