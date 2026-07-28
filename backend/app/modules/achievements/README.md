# Achievements Module

Multi-stage recognition via event-driven progress.

## Consumes

- `ChallengeCompleted`, `ProgressUpdated`, `TrophyAwarded`

## Publishes

- `AchievementUnlocked`

## API

- `GET /api/v1/achievements`
- `GET /api/v1/achievements/me`
- `GET /api/v1/achievements/{achievementId}`
- `POST /api/v1/achievements` (admin)
