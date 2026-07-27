# Level Feature Specification

Version: 1.0

Status: Living Document

Module: Levels

Related Documents

- docs/features/categories.md
- docs/features/challenges.md
- docs/features/progress.md
- docs/product/Requirements.md
- docs/architecture/DataModel.md
- docs/architecture/API.md

---

# Purpose

The Levels module organizes learning progression within a category.

Each level represents a meaningful stage of mastery and groups related challenges that build upon previously acquired knowledge.

Levels define progression, unlocking, and sequencing, but they do not evaluate challenge completion.

---

# Scope

## Included

- Level management
- Learning progression
- Unlock rules
- Level ordering
- Level visibility
- Level metadata

## Excluded

- Challenge evaluation
- Scoring
- Trophy assignment
- User authentication
- Progress calculation

---

# Actors

## Learner

Can:

- View unlocked levels
- View completed levels
- Browse challenges in unlocked levels
- See completion status

Cannot:

- Skip locked levels
- Modify level configuration

---

## Administrator

Can:

- Create levels
- Edit levels
- Reorder levels
- Hide levels
- Configure unlock requirements

---

# User Stories

## LVL-001

As a learner,

I want to progress through levels in order,

So that I build knowledge gradually.

---

## LVL-002

As a learner,

I want to know why a level is locked,

So that I understand what I need to complete next.

---

## LVL-003

As an administrator,

I want to create new learning levels,

So that I can expand the curriculum.

---

## LVL-004

As an administrator,

I want to reorder levels,

So that the learning path can evolve.

---

# Business Rules

A level:

- Belongs to exactly one category.
- Contains one or more challenges.
- Has a display order.
- Has a visibility status.
- May define unlock requirements.

A category should have at least one level before it is considered publishable.

---

# Learning Progression

Recommended progression names:

- Foundations
- Core Concepts
- Applied Practice
- Advanced Techniques
- Expert Challenges

Level names are configurable and should reflect the curriculum.

---

# Unlock Rules

By default, a level becomes available when the previous level is completed.

Future unlock conditions may include:

- Minimum score
- Required trophies
- Time-based unlocks
- Instructor approval
- Optional prerequisite levels

Unlock logic is evaluated by the Progress module.

---

# Level Status

Supported states:

```
Active

Hidden

Archived (Future)
```

Hidden levels:

- Are not visible to learners.
- Remain visible to administrators.

---

# Display Order

Levels have an explicit display order within a category.

Example:

```
Web Security

1 Foundations

2 Core Concepts

3 Applied Practice

4 Advanced Techniques
```

Display order is independent of the internal identifier.

---

# Level Metadata

Each level contains:

- Name
- Description
- Display order
- Status
- Estimated completion time (optional)
- Recommended prerequisites (optional)

Future metadata may include:

- Difficulty indicator
- Learning objectives
- Completion certificate

---

# Completion Rules

A level is considered complete when:

- Every required challenge in the level has been completed.

Optional challenges should not block completion unless explicitly configured.

Completion is determined by the Progress module.

---

# Visibility Rules

Learners:

- See only unlocked and active levels.

Administrators:

- See all levels.

---

# Permissions

## Learner

Can:

- View unlocked levels
- View level details
- Start challenges within unlocked levels

Cannot:

- Access hidden levels
- Modify levels

---

## Administrator

Can:

- Create levels
- Edit levels
- Hide levels
- Restore levels
- Reorder levels
- Configure unlock requirements

All administrative changes should be audited.

---

# Validation Rules

Name

- Required
- Minimum length
- Maximum length

Display Order

- Integer
- Unique within a category

Description

- Optional
- Maximum length

Unlock Rules

- Must reference valid prerequisite levels when configured.

---

# Failure Scenarios

Examples:

- Duplicate display order within the same category.
- Invalid prerequisite level.
- Learner requests a locked level.
- Unauthorized modification attempt.

All failures should return standardized API responses.

---

# Edge Cases

- Category contains only one level.
- Hidden level between two active levels.
- Administrator reorders levels after learners have already started.
- Optional challenges remain incomplete.
- Circular prerequisite configuration.

The system must prevent invalid progression graphs.

---

# Audit Events

Record:

- Level created
- Level updated
- Level hidden
- Level restored
- Level reordered
- Unlock rule modified

---

# API Resources

Base resource:

```
/api/v1/levels
```

Typical operations:

```
GET /

GET /{levelId}

POST /

PATCH /{levelId}

DELETE /{levelId}

PATCH /{levelId}/order
```

Additional category-specific endpoints may include:

```
GET /categories/{categoryId}/levels
```

Endpoint behavior is defined by the OpenAPI specification.

---

# Data Ownership

Levels owns:

- Name
- Description
- Display order
- Status
- Unlock configuration

Progress information is owned by the Progress module.

Challenge content is owned by the Challenges module.

---

# Dependencies

Levels depends on:

- Categories

It should not depend directly on:

- Progress
- Evaluations
- Leaderboard

Progress references levels rather than the reverse.

---

# Relationships

```
Category

1 ───────────── * Level

Level

1 ───────────── * Challenge
```

Levels do not own submissions or user progress.

---

# Non-Functional Requirements

- Level retrieval should be performant.
- Ordering operations should be transactional.
- Unlock evaluation should scale with large numbers of users.
- Hidden levels must never appear in learner-facing APIs.

---

# Future Enhancements

Potential additions:

- Branching learning paths
- Elective levels
- Parallel progression
- Dynamic unlock conditions
- Personalized recommendations
- AI-generated learning paths
- Localization

These enhancements should build on the existing progression model without changing its core principles.

---

# Acceptance Criteria

Level Listing

- Learners see only active, unlocked levels.
- Levels appear in configured display order.

Level Progression

- Completing required challenges unlocks the next level.
- Locked levels clearly communicate their prerequisites.

Administration

- Administrators can create, edit, reorder, hide, and restore levels.
- Invalid prerequisite configurations are rejected.

---

# Guiding Principle

A Level answers the question:

**"What stage of mastery am I currently working toward?"**

Levels should create a structured, motivating learning journey by grouping related challenges into meaningful milestones and guiding learners from foundational knowledge to advanced capability.