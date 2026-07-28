# Leaderboards Module

Read-only XP ranking projection.

## Consumes

- `ProgressUpdated`

## API

- `GET /api/v1/leaderboards?period=all_time|weekly|monthly`
- `GET /api/v1/leaderboards/me`

## Rules

- Never writes Progress/XP source
- Rebuildable from `ProgressUpdated` events
