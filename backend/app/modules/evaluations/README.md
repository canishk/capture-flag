# Evaluations Module

## Purpose

Evaluate submissions via pluggable strategies.

## Responsibilities

- Strategy execution, result recording, pass/fail, feedback

## Does NOT own

- Submissions (immutable), progress, unlocks

## Public API

- `GET /api/v1/evaluations/strategies` (admin)
- `POST /api/v1/evaluations/preview` (admin)
- `GET /api/v1/evaluations/submission/{submissionId}` (admin)

## Strategies (v1)

- `exact_match`, `regex`, `numeric_range`

## Dependencies

- `SubmissionService`, `ChallengeService`

## Events

- `EvaluationCompleted`, `EvaluationFailed`

## Flow

`SubmissionCreated` → auto-evaluate → update submission status → publish evaluation event
