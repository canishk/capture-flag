# Progress Feature Specification

Version: 1.0

Status: Living Document

Module: Progress

Related Documents

- docs/features/challenges.md
- docs/features/evaluations.md
- docs/features/submissions.md
- docs/features/trophies.md
- docs/features/leaderboard.md
- docs/architecture/EventModel.md
- docs/architecture/DataModel.md

---

# Purpose

The Progress module maintains the learner's current learning state.

Rather than storing raw learning activity, it consumes domain events and derives the learner's current progress across challenges, levels, categories, and the overall platform.

Progress is a projection of historical events.

---

# Scope

## Included

- Challenge completion
- Level completion
- Category completion
- Learning statistics
- XP calculation
- Unlock state
- Learning history summary

## Excluded

- Submission storage
- Evaluation logic
- Trophy rules
- Leaderboard ranking
- Challenge content

---

# Design Principles

The Progress module follows these principles:

- Event-driven
- Derived state
- Eventually consistent
- Rebuildable
- Fast to query

Progress should never become the source of truth.

---

# Actors

## Learner

Can:

- View personal progress
- View completed challenges
- View learning statistics
- View XP
- View unlocked content
- Resume learning

Cannot:

- Modify progress

---

## Administrator

Can:

- View learner progress
- Recalculate progress
- Rebuild projections
- Diagnose inconsistencies

Cannot:

- Manually edit learner progress

---

# User Stories

## PROG-001

As a learner,

I want to see my learning progress,

So that I know how far I have come.

---

## PROG-002

As a learner,

I want completed challenges to unlock new content,

So that I can continue learning.

---

## PROG-003

As an administrator,

I want progress to be rebuildable,

So that system errors can be corrected without data loss.

---

## PROG-004

As an administrator,

I want progress statistics,

So that platform engagement can be measured.

---

# Responsibilities

The Progress module determines:

- Completed challenges
- Completed levels
- Completed categories
- Current XP
- Current learning streak (future)
- Current unlocks
- Completion percentages

---

# Progress Sources

Progress is derived from:

- SubmissionEvaluated
- EvaluationPassed
- EvaluationFailed
- HintViewed
- ChallengePublished
- ChallengeArchived

Future sources:

- AI Tutor Completed
- ResourceViewed
- Learning Path Completed

---

# Learning State

Each learner has:

```
Current XP

Completed Challenges

Completed Levels

Completed Categories

Unlocked Levels

Unlocked Challenges

Completion Percentage
```

---

# Challenge Completion

A challenge is complete when:

- At least one successful evaluation exists.

The first successful evaluation marks completion.

Subsequent successful submissions do not create additional completions.

---

# Level Completion

A level is complete when:

- Every required challenge has been completed.

Optional challenges do not block completion unless configured.

---

# Category Completion

A category is complete when:

- Every required level is complete.

---

# Unlock Rules

Progress evaluates unlock conditions.

Examples:

Complete:

```
Level 1
```

↓

Unlock:

```
Level 2
```

Future unlock conditions:

- XP thresholds
- Trophy ownership
- AI recommendations
- Instructor approval
- Time-based unlocks

---

# XP

Version 1

XP equals the sum of earned challenge XP.

Example:

```
Challenge A

100 XP

Challenge B

50 XP

Challenge C

150 XP

Total

300 XP
```

Future XP modifiers:

- Hint penalties
- Speed bonus
- First attempt bonus
- Daily streak bonus

---

# Statistics

Examples:

- Challenges attempted
- Challenges completed
- Submission count
- Success rate
- Hint usage
- Average attempts
- Resources viewed
- Time spent learning (future)

Statistics are derived rather than manually maintained.

---

# Completion Percentage

Example:

```
Completed Challenges

18

Total Challenges

24

Completion

75%
```

Completion calculations should be configurable.

---

# Learning Resume

The module should provide:

- Last active challenge
- Recently viewed resources
- Recently viewed hints

This enables learners to resume quickly.

---

# Progress Events

The module publishes:

```
ProgressUpdated

ChallengeCompleted

LevelCompleted

CategoryCompleted
```

Subscribers include:

- Trophies
- Leaderboard
- Analytics
- Notifications

---

# Projection Rebuild

Progress projections must be rebuildable.

Process:

```
Submission History

↓

Evaluation Results

↓

Replay Events

↓

Recalculate Progress
```

Rebuilds should produce deterministic results.

---

# Failure Scenarios

Examples:

- Missing events
- Duplicate events
- Event replay
- Challenge archived
- XP recalculation

The module should tolerate duplicate events.

---

# Edge Cases

- Challenge deleted after completion
- Challenge moved to another level
- Evaluation rules change
- Replay after bug fix
- Learner retries completed challenge

Previously completed work should remain valid unless an administrator explicitly initiates a recalculation.

---

# Security

Learners may access only their own progress.

Administrators may access platform-wide progress.

Progress projections should never expose:

- Submission contents
- Evaluation configuration
- Secrets

---

# Audit

Record:

- Projection rebuild
- Manual recalculation
- Unlock events
- Completion events

Audit data is separate from learner statistics.

---

# API Resources

Base resource:

```
/api/v1/progress
```

Typical operations:

```
GET /me

GET /summary

GET /statistics

GET /category/{categoryId}

GET /level/{levelId}

GET /challenge/{challengeId}
```

Administrative operations:

```
POST /rebuild

POST /recalculate

GET /diagnostics
```

The OpenAPI specification defines the canonical API.

---

# Data Ownership

Progress owns:

- Current XP
- Completion state
- Unlock state
- Derived statistics

Submissions own:

- Attempt history

Evaluations own:

- Pass/fail results

Challenges own:

- XP configuration

---

# Dependencies

Progress depends on:

- Challenges
- Evaluations
- Submissions

Progress should not depend on:

- Leaderboard
- Trophies
- Notifications

Those modules consume Progress events.

---

# Relationships

```
User

1 ───────────── 1 Progress Projection

Progress

1 ───────────── * Completed Challenge

Progress

1 ───────────── * Completed Level

Progress

1 ───────────── * Completed Category
```

---

# Non-Functional Requirements

- Progress queries should be optimized for read performance.
- Projection rebuilds should support batch execution.
- Event replay should be deterministic.
- Duplicate events must not create duplicate completions.
- Progress calculations should scale to large learner populations.

---

# Future Enhancements

Potential additions:

- Learning streaks
- Daily goals
- Weekly goals
- Adaptive progression
- AI learning recommendations
- Learning paths
- Skill trees
- Mastery levels
- Personalized dashboards

These enhancements should build upon the projection model.

---

# Acceptance Criteria

Challenge Progress

- Successful evaluations complete challenges.
- Duplicate successful submissions do not create duplicate completions.

Level Progress

- Completing required challenges unlocks the next level.
- Completion percentages update automatically.

Projection

- Progress can be rebuilt from historical events.
- Rebuilt projections match live projections.

Security

- Learners can access only their own progress.
- Administrators can rebuild projections.

---

# Guiding Principle

Progress answers the question:

**"Where is this learner right now?"**

It is a derived, query-optimized projection of historical learning activity, providing an accurate and efficient view of the learner's journey without becoming the authoritative source of that history.