# Trophies Module

Recognition bounded context — trophy definitions and awards.

## Consumes

- `ChallengeCompleted`, `LevelCompleted`, `CategoryCompleted`

## Publishes

- `TrophyAwarded`

## API

- `GET /api/v1/trophies`
- `GET /api/v1/trophies/me`
- `GET /api/v1/trophies/{trophyId}`
- `POST /api/v1/trophies` (admin)

## Rules

- Event-only input — no Progress/Submission repo access
- Idempotent via `ProcessedRecognitionEvent`
- Immutable award history
