# Hint Feature Specification

Version: 1.0

Status: Living Document

Module: Hints

Related Documents

- docs/features/challenges.md
- docs/features/progress.md
- docs/features/evaluations.md
- docs/architecture/EventModel.md
- docs/architecture/API.md

---

# Purpose

The Hints module provides progressive guidance to learners who are struggling with a challenge.

Hints should encourage learning and problem solving without immediately revealing the solution.

Hints are owned by a Challenge but managed as independent entities.

---

# Scope

## Included

- Hint management
- Progressive hint sequencing
- Hint visibility
- Hint penalties
- Hint unlock rules
- Hint analytics

## Excluded

- Challenge content
- Evaluation logic
- Progress calculation
- Scoring algorithms

---

# Design Principles

Hints follow these principles:

- Progressive disclosure
- Learning before answers
- Independent configuration
- Optional usage
- Analytics-friendly

Hints should guide thinking rather than provide direct solutions whenever possible.

---

# Actors

## Learner

Can:

- View available hints
- Reveal additional hints
- Review previously viewed hints

Cannot:

- Modify hints
- Skip unlock requirements

---

## Administrator

Can:

- Create hints
- Edit hints
- Delete hints
- Reorder hints
- Configure penalties
- Configure unlock rules

---

# User Stories

## HINT-001

As a learner,

I want progressively more helpful hints,

So that I can continue learning without immediately seeing the answer.

---

## HINT-002

As a learner,

I want to know whether using a hint affects my score,

So that I can make an informed decision.

---

## HINT-003

As an administrator,

I want to control the order of hints,

So that guidance follows the intended learning path.

---

## HINT-004

As an administrator,

I want to understand which hints are frequently used,

So that I can improve challenge quality.

---

# Hint Lifecycle

```
Draft

↓

Published

↓

Hidden

↓

Archived
```

Only published hints are available to learners.

---

# Hint Levels

Recommended progression:

```
Hint 1

Learning Nudge
```

Example:

> What part of the HTTP request controls authentication?

---

```
Hint 2

Concept Reminder
```

Example:

> Review how SQL queries are constructed from user input.

---

```
Hint 3

Method
```

Example:

> Consider what happens when a quote terminates a SQL string.

---

```
Hint 4

Almost There
```

Example:

> Authentication can sometimes be bypassed by making the WHERE clause always evaluate to TRUE.

---

```
Hint 5 (Optional)

Solution Walkthrough
```

Normally disabled in Version 1.

---

# Hint Structure

Each hint contains:

- Title
- Hint text
- Display order
- Penalty configuration
- Unlock rule
- Status

Optional:

- Images
- Code snippets
- Links
- Embedded videos (future)

---

# Hint Ordering

Hints are ordered explicitly.

Example:

```
1

Learning Nudge

↓

2

Concept Reminder

↓

3

Method

↓

4

Almost There
```

Administrators may reorder hints.

---

# Hint Visibility

States:

```
Draft

Published

Hidden

Archived
```

Hidden hints are visible only to administrators.

---

# Unlock Rules

Version 1 supports:

- Manual reveal
- Previous hint viewed

Future support:

- Time elapsed
- Number of failed submissions
- AI recommendation
- Instructor release

Unlock logic should be configurable.

---

# Penalty Configuration

Each hint may define:

- Score reduction
- Percentage reduction
- No penalty

Example:

```
Hint 1

No penalty

Hint 2

-5 points

Hint 3

-10 points
```

Penalty calculation belongs to the Progress module.

Hints define configuration only.

---

# Learning Philosophy

Hints should:

- Encourage exploration
- Reinforce concepts
- Avoid revealing exact answers
- Increase learner confidence

Hints should not become substitute solutions.

---

# Analytics

Useful metrics include:

- Hint view count
- Hint sequence reached
- Average hints per learner
- Hint effectiveness
- Challenge abandonment after hints

Analytics are consumed by the Analytics module.

---

# Events

The Hints module publishes:

```
HintViewed

HintUnlocked
```

Potential subscribers:

- Progress
- Analytics
- Notifications (future)

---

# Validation Rules

Hint text

- Required
- Maximum length

Display order

- Unique within a challenge

Penalty

- Non-negative

Unlock configuration

- Valid prerequisite hint

---

# Failure Scenarios

Examples:

- Hidden hint requested
- Invalid display order
- Invalid unlock dependency
- Learner requests unavailable hint

Errors should return standardized API responses.

---

# Edge Cases

- Challenge with no hints
- Challenge with one hint
- Simultaneous reveal requests
- Hidden hint between published hints
- Reordered hints after learners have started

Previously viewed hints should remain available to the learner.

---

# Security

Hints should never expose:

- Protected answers
- Evaluation configuration
- Internal notes
- Administrator comments

Hint content should be reviewed before publication.

---

# Audit

Record:

- Hint created
- Hint updated
- Hint published
- Hint hidden
- Hint reordered

Hint views are tracked separately as learner activity.

---

# API Resources

Base resource:

```
/api/v1/hints
```

Typical operations:

```
GET /challenge/{challengeId}

GET /{hintId}

POST /

PATCH /{hintId}

DELETE /{hintId}

POST /{hintId}/reveal
```

Challenge-specific management:

```
PATCH /challenge/{challengeId}/order
```

The OpenAPI specification defines the canonical API.

---

# Data Ownership

Hints owns:

- Hint content
- Display order
- Unlock rules
- Penalty configuration
- Status

Progress owns:

- Score adjustment
- Completion state

Challenges owns:

- Challenge metadata

---

# Dependencies

Hints depends on:

- Challenges

Hints should not depend directly on:

- Progress
- Evaluations
- Leaderboard

Communication occurs through domain events.

---

# Relationships

```
Challenge

1 ───────────── * Hint
```

Hints are children of a Challenge but remain individually configurable.

---

# Non-Functional Requirements

- Hint retrieval should be fast.
- Reveal operations should be idempotent.
- Hint ordering should be transactional.
- Viewed hints should remain accessible.
- Hint analytics should be collected efficiently.

---

# Future Enhancements

Potential additions:

- AI-generated hints
- Adaptive hints
- Personalized hints
- Multimedia hints
- Interactive hints
- Instructor hints
- Community-contributed hints
- Hint ratings
- Hint translations

These enhancements should extend the existing hint model without changing its core behavior.

---

# Acceptance Criteria

Hint Management

- Administrators can create, edit, reorder, publish, hide, and archive hints.

Learner Experience

- Learners can reveal hints according to configured rules.
- Viewed hints remain accessible.
- Hint penalties are clearly communicated.

Analytics

- Hint views generate events.
- Hint usage can be analyzed to improve challenge quality.

---

# Guiding Principle

A Hint answers the question:

**"What is the smallest piece of guidance that helps the learner make the next step on their own?"**

Hints should progressively support understanding while preserving the challenge's educational value. They are learning tools—not shortcuts to the answer.