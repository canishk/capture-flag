# Leaderboard Feature Specification

Version: 1.0

Status: Living Document

Module: Leaderboard

Related Documents

- docs/features/progress.md
- docs/features/trophies.md
- docs/features/challenges.md
- docs/architecture/EventModel.md
- docs/architecture/DataModel.md

---

# Purpose

The Leaderboard module ranks learners based on configurable scoring rules to encourage engagement and recognize achievement.

Leaderboards provide a read-optimized view of learner rankings and should never become the authoritative source of learner progress.

---

# Scope

## Included

- Global rankings
- Category rankings
- Time-based rankings
- Ranking history
- Rank calculation
- Public leaderboard views

## Excluded

- Progress calculation
- XP calculation
- Submission evaluation
- Trophy awarding

---

# Design Principles

The Leaderboard module follows these principles:

- Read optimized
- Event driven
- Rebuildable
- Configurable
- Fair

Leaderboards are projections derived from learner activity.

---

# Actors

## Learner

Can:

- View public leaderboards
- View personal ranking
- View nearby rankings
- Filter leaderboards

Cannot:

- Modify rankings

---

## Administrator

Can:

- Configure leaderboard rules
- Rebuild rankings
- Reset seasonal leaderboards
- Hide learners when required
- View leaderboard analytics

---

# User Stories

## LEADER-001

As a learner,

I want to compare my progress with others,

So that I remain motivated.

---

## LEADER-002

As a learner,

I want to see nearby rankings,

So that I know what I need to improve.

---

## LEADER-003

As an administrator,

I want multiple leaderboard types,

So that different learning goals can be encouraged.

---

## LEADER-004

As an administrator,

I want seasonal resets,

So that new learners remain competitive.

---

# Leaderboard Types

Version 1

## Global

Ranks every learner.

---

## Category

Ranks learners within a category.

Examples:

- Web Security
- Cryptography
- Networking

---

## Weekly

Resets every week.

---

## Monthly

Resets every month.

---

Future:

- Daily
- Organization
- Team
- Friends
- Country
- Skill-based
- Tournament
- Event

---

# Ranking Metric

Version 1

Ranking order:

1. Total XP
2. Completed Challenges
3. Earliest Completion Timestamp
4. User ID (stable tie-breaker)

The ranking algorithm should be configurable.

---

# Ranking Entry

Each entry contains:

- Rank
- Learner
- XP
- Challenges Completed
- Levels Completed
- Categories Completed
- Trophy Count
- Last Updated

Optional:

- Avatar
- Organization
- Country
- Streak

---

# Personal Position

Learners should always be able to view:

- Current rank
- Previous rank
- Rank movement
- Next learner above
- Next learner below

Example:

```
Rank 128

↑ +4

Need 40 XP to reach Rank 127
```

---

# Ranking Updates

Leaderboards update when relevant events occur.

Examples:

```
ChallengeCompleted

↓

ProgressUpdated

↓

Leaderboard Updated
```

Updates should be asynchronous where possible.

---

# Seasonal Leaderboards

Seasonal leaderboards support:

- Start date
- End date
- Automatic reset
- Historical archive

Historical rankings remain available for reporting.

---

# Visibility

Leaderboards may be:

```
Public

Authenticated

Private

Disabled
```

Visibility is configurable.

---

# Privacy

Learners may choose:

- Display full profile
- Display nickname
- Display anonymous alias

Opt-out behavior should be configurable according to platform policy.

---

# Events

The module subscribes to:

```
ProgressUpdated

ChallengeCompleted

LevelCompleted

CategoryCompleted

TrophyAwarded
```

The module publishes:

```
LeaderboardUpdated

LeaderboardReset
```

Subscribers may include:

- Analytics
- Notifications

---

# Projection Rebuild

Leaderboards must support rebuilding.

Process:

```
Progress Projection

↓

Replay Rankings

↓

Leaderboard Projection
```

Rebuilds should produce deterministic results.

---

# Validation Rules

Ranking configuration

- Valid metric
- Valid tie-breaker
- Valid reset schedule

Leaderboard

- Unique identifier
- Valid visibility

---

# Failure Scenarios

Examples:

- Missing progress events
- Duplicate events
- Reset interrupted
- Ranking corruption

Ranking failures must never affect learner progress.

---

# Edge Cases

- Two learners with identical scores
- Learner deleted
- Learner hidden
- Seasonal reset during active learning
- XP recalculation

Tie-breaking must produce stable rankings.

---

# Security

Learners:

- May view leaderboards according to visibility rules.

Administrators:

- May manage leaderboard configuration.

Internal ranking calculations should not expose implementation details.

---

# Audit

Record:

- Leaderboard created
- Leaderboard updated
- Leaderboard rebuilt
- Leaderboard reset
- Configuration changes

Ranking history is stored separately.

---

# API Resources

Base resource:

```
/api/v1/leaderboards
```

Typical operations:

```
GET /

GET /{leaderboardId}

GET /global

GET /category/{categoryId}

GET /weekly

GET /monthly

GET /me

GET /nearby
```

Administrative operations:

```
POST /rebuild

POST /reset

PATCH /configuration
```

The OpenAPI specification is the authoritative API contract.

---

# Data Ownership

Leaderboards owns:

- Ranking projections
- Ranking history
- Configuration
- Seasonal archives

Progress owns:

- Learner progression

Trophies own:

- Achievement history

---

# Dependencies

Leaderboards depends on:

- Progress
- Trophy events

Leaderboards should not depend directly on:

- Evaluations
- Submissions
- Challenge content

---

# Relationships

```
Leaderboard

1 ───────────── * Leaderboard Entry

User

1 ───────────── * Leaderboard Entry
```

A leaderboard contains many entries.

A learner may appear on many leaderboards.

---

# Non-Functional Requirements

- Ranking queries should be optimized for high read throughput.
- Updates should be asynchronous.
- Rebuilds should support batch execution.
- Pagination should be efficient.
- Ranking calculations should scale to millions of learners.

---

# Future Enhancements

Potential additions:

- Team rankings
- Friends leaderboard
- AI-powered recommendations
- Seasonal rewards
- Regional rankings
- Skill-specific rankings
- Anti-cheat anomaly detection
- Ranking snapshots
- Tournament mode

These enhancements should build upon the projection model.

---

# Acceptance Criteria

Leaderboard Management

- Administrators can configure and rebuild leaderboards.
- Seasonal resets archive historical rankings.

Learner Experience

- Learners can view global, category, weekly, and monthly rankings.
- Nearby rankings display neighboring learners.
- Rank movement is visible after updates.

Projection

- Leaderboards rebuild deterministically.
- Duplicate events do not create inconsistent rankings.

Security

- Visibility rules are enforced.
- Hidden learners are excluded according to configuration.

---

# Guiding Principle

A Leaderboard answers the question:

**"How does this learner currently rank compared with others?"**

Leaderboards are read-optimized projections that transform learner progress into meaningful rankings while remaining independent of submissions, evaluations, and other write-side learning workflows.