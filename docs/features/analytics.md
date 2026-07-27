# Analytics Feature Specification

Version: 1.0

Status: Living Document

Module: Analytics

Related Documents

- docs/features/progress.md
- docs/features/submissions.md
- docs/features/evaluations.md
- docs/features/hints.md
- docs/features/resources.md
- docs/features/leaderboard.md
- docs/architecture/EventModel.md
- docs/architecture/DataModel.md

---

# Purpose

The Analytics module transforms learner activity into actionable insights for administrators, instructors, and content authors.

Unlike Progress, which answers the current state of a learner, Analytics explains trends, bottlenecks, engagement, and content quality across the platform.

Analytics is a read-only projection built from domain events.

---

# Scope

## Included

- Platform analytics
- Challenge analytics
- Learner analytics
- Category analytics
- Resource analytics
- Hint analytics
- Evaluation analytics
- Time-based reporting
- Trend analysis

## Excluded

- Progress calculation
- Leaderboard ranking
- Trophy awarding
- Submission storage
- Evaluation execution

---

# Design Principles

Analytics follows these principles:

- Event-driven
- Read optimized
- Aggregated
- Rebuildable
- Privacy aware

Analytics should never become the source of truth.

---

# Actors

## Learner

Can:

- View personal learning statistics
- View personal activity trends
- View improvement over time

Cannot:

- Access platform analytics
- Access other learners' data

---

## Instructor / Content Author

Can:

- View challenge analytics
- View hint effectiveness
- View resource usage
- View evaluation statistics
- Identify difficult content

---

## Administrator

Can:

- View platform-wide analytics
- Export reports
- Configure dashboards
- Rebuild analytics projections

---

# User Stories

## ANALYTICS-001

As an instructor,

I want to know which challenges learners struggle with,

So that I can improve challenge quality.

---

## ANALYTICS-002

As an administrator,

I want engagement statistics,

So that I understand platform usage.

---

## ANALYTICS-003

As a learner,

I want to see my learning trends,

So that I stay motivated.

---

## ANALYTICS-004

As a content author,

I want hint effectiveness metrics,

So that I know whether hints are helpful.

---

# Analytics Categories

## Learner Analytics

Examples:

- Total XP
- Completed challenges
- Attempts
- Success rate
- Average attempts
- Learning time
- Resources viewed
- Hint usage

---

## Challenge Analytics

Examples:

- Attempt count
- Completion rate
- Average attempts
- Average completion time
- Abandonment rate
- Hint usage
- Resource usage
- Failure distribution

---

## Level Analytics

Examples:

- Completion rate
- Average completion time
- Learner progression
- Drop-off rate

---

## Category Analytics

Examples:

- Popular categories
- Completion rate
- Average learner progression

---

## Resource Analytics

Examples:

- Views
- Downloads
- Click-through rate
- Resource effectiveness
- Most viewed resources

---

## Hint Analytics

Examples:

- Reveal count
- Hint progression
- Average hint level reached
- Completion after hint
- Hint abandonment

---

## Evaluation Analytics

Examples:

- Strategy usage
- Pass rate
- Failure reasons
- Average evaluation time
- Timeout rate
- AI evaluation usage

---

## Platform Analytics

Examples:

- Daily active learners
- Weekly active learners
- Monthly active learners
- New registrations
- Active challenges
- Active categories

---

# Time Dimensions

Analytics should support:

- Today
- Yesterday
- Last 7 days
- Last 30 days
- This month
- This year
- Custom range

Future:

- Academic term
- Season
- Event

---

# Learning Funnel

Example:

```
Started Challenge

↓

Submitted Answer

↓

Viewed Hint

↓

Viewed Resource

↓

Passed Challenge

↓

Completed Level
```

The funnel identifies where learners leave the learning journey.

---

# Challenge Health Score

Each challenge should expose a health score.

Example inputs:

- Completion rate
- Hint usage
- Resource usage
- Failure rate
- Average attempts
- Learner feedback (Future)

The score helps prioritize content improvements.

---

# Resource Effectiveness

Analytics should correlate:

```
Viewed Resource

↓

Completed Challenge
```

Possible metrics:

- Completion after viewing
- Improvement in success rate
- Average attempts before/after

Correlation should not imply causation and should be clearly labeled as an observed relationship.

---

# Hint Effectiveness

Analytics should measure:

- Hint views
- Hint progression
- Completion after hint
- Additional attempts after hint
- Average improvement

These metrics support continuous refinement of hint quality.

---

# Event Sources

Analytics subscribes to:

```
SubmissionCreated

SubmissionEvaluated

ChallengeCompleted

LevelCompleted

CategoryCompleted

HintViewed

ResourceViewed

ResourceDownloaded

ProgressUpdated

TrophyAwarded
```

Future:

```
AITutorCompleted

RecommendationAccepted

LearningSessionStarted

LearningSessionEnded
```

---

# Dashboards

Recommended dashboards:

## Platform Overview

- Active learners
- Completion rate
- New learners
- XP earned
- Challenge activity

---

## Challenge Dashboard

- Attempts
- Pass rate
- Average attempts
- Failure breakdown
- Hint usage

---

## Learner Dashboard

- Progress trend
- XP trend
- Completed challenges
- Activity calendar

---

## Content Dashboard

- Resource usage
- Hint effectiveness
- Challenge health
- Evaluation performance

---

# Privacy

Analytics must support:

- Aggregated reporting
- Role-based access
- Data anonymization where appropriate

Personally identifiable information should be minimized in platform-wide reports.

---

# Projection Rebuild

Analytics must support deterministic rebuilds.

Process:

```
Replay Domain Events

↓

Recalculate Aggregations

↓

Rebuild Dashboards
```

---

# Validation Rules

Dashboard configuration

- Valid metrics
- Valid date ranges
- Valid filters

Analytics queries

- Authorized
- Bounded date range
- Supported dimensions

---

# Failure Scenarios

Examples:

- Missing events
- Duplicate events
- Delayed events
- Projection corruption
- Dashboard timeout

Analytics failures must never impact learner workflows.

---

# Edge Cases

- Challenge deleted after historical activity
- Resource updated
- Hint reordered
- Event replay
- Time zone changes
- Seasonal resets

Historical analytics should remain reproducible where possible.

---

# Security

Learners

- Access only their personal analytics

Instructors

- Access analytics for authorized content

Administrators

- Access platform analytics

Exports should respect role permissions.

---

# Audit

Record:

- Dashboard configuration changes
- Projection rebuilds
- Report exports
- Scheduled report execution

Audit records are separate from analytical data.

---

# API Resources

Base resource:

```
/api/v1/analytics
```

Typical operations:

```
GET /platform

GET /learner/me

GET /challenge/{challengeId}

GET /category/{categoryId}

GET /level/{levelId}

GET /resource/{resourceId}

GET /hint/{hintId}

GET /dashboard/{dashboardId}
```

Administrative operations:

```
POST /rebuild

POST /export

GET /health

GET /trends
```

The OpenAPI specification defines the canonical API.

---

# Data Ownership

Analytics owns:

- Aggregated metrics
- Historical trends
- Dashboards
- Reports
- Derived KPIs

Progress owns:

- Current learner state

Leaderboards own:

- Rankings

Submissions own:

- Attempt history

Evaluations own:

- Evaluation outcomes

---

# Dependencies

Analytics depends on:

- Domain events
- Projection infrastructure

Analytics should not depend directly on business modules for calculations.

---

# Relationships

```
Domain Events

1 ───────────── * Analytics Projection

Analytics Projection

1 ───────────── * Dashboard

Dashboard

1 ───────────── * Widget
```

---

# Non-Functional Requirements

- Dashboard queries should complete within defined performance targets.
- Large aggregations should execute asynchronously where appropriate.
- Metrics should support incremental updates.
- Rebuilds should support batch processing.
- Historical data should remain queryable for long-term trend analysis.

---

# Future Enhancements

Potential additions:

- Predictive analytics
- AI-generated insights
- Anomaly detection
- Cohort analysis
- Learning path analytics
- Recommendation effectiveness
- Heatmaps
- Instructor benchmarking
- Scheduled reports

These enhancements should extend the projection model without changing the event architecture.

---

# Acceptance Criteria

Analytics Projection

- Metrics are derived from domain events.
- Rebuilds produce deterministic results.

Dashboards

- Platform, learner, challenge, and content dashboards are available.
- Role-based access is enforced.

Insights

- Challenge health scores are calculated.
- Hint and resource effectiveness metrics are available.
- Learning funnels identify common drop-off points.

Security

- Learners access only their own analytics.
- Administrative reports respect authorization rules.

---

# Guiding Principle

Analytics answers the question:

**"What can we learn from how people learn?"**

It transforms raw learner activity into meaningful insights that improve educational content, platform quality, and learner outcomes while remaining a read-only, event-driven projection.