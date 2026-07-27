# Trophy Feature Specification

Version: 1.0

Status: Living Document

Module: Trophies

Related Documents

- docs/features/progress.md
- docs/features/challenges.md
- docs/features/submissions.md
- docs/architecture/EventModel.md
- docs/architecture/DataModel.md

---

# Purpose

The Trophies module recognizes learner achievements by awarding trophies when predefined criteria are met.

Trophies motivate learners, celebrate milestones, and encourage exploration beyond mandatory progression.

The module determines achievements independently by subscribing to domain events.

---

# Scope

## Included

- Trophy definitions
- Trophy criteria
- Trophy evaluation
- Trophy awarding
- Trophy history
- Trophy presentation

## Excluded

- Progress calculation
- Leaderboard ranking
- XP calculation
- Challenge evaluation
- Submission storage

---

# Design Principles

The Trophies module follows these principles:

- Event-driven
- Rule-based
- Independent
- Idempotent
- Auditable

Trophies should never modify learner progress.

---

# Actors

## Learner

Can:

- View earned trophies
- Browse available trophies
- View trophy requirements (configurable)
- Share trophies (Future)

Cannot:

- Award trophies
- Remove trophies

---

## Administrator

Can:

- Create trophy definitions
- Edit trophy metadata
- Enable or disable trophies
- Configure trophy rules
- View award statistics

Cannot:

- Manually award trophies (except administrative override)

---

# User Stories

## TROPHY-001

As a learner,

I want recognition for important milestones,

So that I feel motivated to continue learning.

---

## TROPHY-002

As a learner,

I want to see how a trophy was earned,

So that I understand my accomplishments.

---

## TROPHY-003

As an administrator,

I want configurable achievement rules,

So that new trophies can be introduced without changing application code.

---

## TROPHY-004

As an administrator,

I want trophy analytics,

So that I understand learner engagement.

---

# Trophy Lifecycle

```
Draft

↓

Published

↓

Hidden

↓

Archived
```

Only published trophies may be awarded.

---

# Trophy Structure

Each trophy contains:

- Name
- Description
- Icon
- Category
- Rarity
- Rule
- Visibility
- Status

Optional:

- Badge color
- Animation
- Display priority
- Expiration (Future)

---

# Trophy Categories

Suggested categories:

- Progress
- Skill
- Exploration
- Consistency
- Community (Future)
- Special Event (Future)

---

# Rarity

Recommended values:

- Common
- Uncommon
- Rare
- Epic
- Legendary

Rarity is informational and does not affect progression.

---

# Trophy Rules

Version 1 supports:

## First Achievement

Example:

Complete first challenge.

---

## Completion Count

Examples:

- Complete 10 challenges.
- Complete 100 challenges.
- Complete every challenge in a category.

---

## Category Mastery

Examples:

- Complete Web Security.
- Complete Cryptography.
- Complete Networking.

---

## Level Mastery

Examples:

- Complete Foundations.
- Complete Advanced Techniques.

---

## Performance

Examples:

- Complete on first attempt.
- Complete without hints.
- Complete within a time limit (Future).

---

## Exploration

Examples:

- View 20 learning resources.
- Reveal first hint.
- Explore every category.

---

Future rule types:

- AI Tutor milestones
- Learning streaks
- Community contributions
- Seasonal events

---

# Rule Evaluation

Rules are evaluated when relevant events occur.

Examples:

```
ChallengeCompleted
```

↓

Evaluate:

- First Challenge
- Challenge Count
- Category Progress

---

```
LevelCompleted
```

↓

Evaluate:

- Level Mastery

---

```
CategoryCompleted
```

↓

Evaluate:

- Category Master

---

# Awarding

A learner may earn a trophy only once.

Awarding is atomic.

Duplicate events must never produce duplicate trophies.

---

# Trophy Visibility

Visibility options:

```
Visible

Hidden

Secret
```

Visible

- Trophy and requirements are displayed.

Hidden

- Trophy exists but is not displayed.

Secret

- Trophy is hidden until earned.

---

# Notifications

Future integrations:

- Toast notification
- Email
- Push notification
- Achievement timeline

Notifications subscribe to TrophyAwarded events.

---

# Trophy History

Each award records:

- Trophy
- Learner
- Awarded timestamp
- Triggering event
- Trigger metadata

Award history is immutable.

---

# Events

The module subscribes to:

```
ChallengeCompleted

LevelCompleted

CategoryCompleted

ProgressUpdated
```

The module publishes:

```
TrophyAwarded
```

Subscribers may include:

- Notifications
- Analytics
- Leaderboard (Future)

---

# Validation Rules

Name

- Required
- Unique

Rule

- Required
- Valid

Icon

- Required

Category

- Required

---

# Failure Scenarios

Examples:

- Invalid rule configuration
- Duplicate trophy
- Missing event
- Unknown rule type

Award processing should fail safely without affecting learner progress.

---

# Edge Cases

- Rule updated after learners already earned a trophy.
- Trophy disabled.
- Event replay.
- Duplicate event delivery.
- Rebuilt progress projection.

Previously awarded trophies should remain unless an administrator explicitly revokes them.

---

# Security

Learners:

- May view only their own earned trophies.

Administrators:

- May manage trophy definitions.

Award rules should not expose internal implementation details.

---

# Audit

Record:

- Trophy created
- Trophy updated
- Trophy published
- Trophy awarded
- Trophy revoked (administrative)

Award history is separate from administrative audit logs.

---

# API Resources

Base resource:

```
/api/v1/trophies
```

Typical operations:

```
GET /

GET /{trophyId}

GET /me

POST /

PATCH /{trophyId}

DELETE /{trophyId}
```

Administrative operations:

```
POST /preview-rule

POST /simulate-award
```

The OpenAPI specification is the authoritative API contract.

---

# Data Ownership

Trophies owns:

- Trophy definitions
- Trophy rules
- Award history
- Visibility

Progress owns:

- Completion state

Challenges own:

- Challenge metadata

---

# Dependencies

Trophies depends on:

- Progress events
- Challenge events

It should not depend directly on:

- Leaderboard
- Notifications
- Analytics

Communication occurs through domain events.

---

# Relationships

```
Trophy

1 ───────────── * Trophy Award

User

1 ───────────── * Trophy Award
```

A trophy may be awarded to many learners.

A learner may earn many trophies.

---

# Non-Functional Requirements

- Trophy evaluation should be lightweight.
- Award processing should be idempotent.
- Trophy queries should support pagination.
- Award history should be immutable.
- Rule evaluation should be extensible.

---

# Future Enhancements

Potential additions:

- Trophy series
- Progressive achievements
- Hidden achievements
- Seasonal trophies
- Organization trophies
- Team trophies
- AI-generated achievements
- Collectible sets
- Trophy marketplace (cosmetic only)

These enhancements should extend the rule engine without changing the event model.

---

# Acceptance Criteria

Trophy Management

- Administrators can create, edit, publish, hide, and archive trophies.
- Invalid trophy rules are rejected.

Awarding

- Eligible learners receive trophies automatically.
- Duplicate events do not create duplicate awards.
- Secret trophies remain hidden until earned.

History

- Every award is recorded with its triggering event.
- Award history cannot be modified.

---

# Guiding Principle

A Trophy answers the question:

**"What meaningful accomplishment has this learner achieved?"**

Trophies should recognize learning milestones through independently evaluated, event-driven rules, celebrating achievement without becoming part of the core progression logic.