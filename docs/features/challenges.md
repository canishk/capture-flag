# Challenge Feature Specification

Version: 1.0

Status: Living Document

Module: Challenges

Related Documents

- docs/features/categories.md
- docs/features/levels.md
- docs/features/progress.md
- docs/features/evaluations.md
- docs/architecture/DataModel.md
- docs/architecture/API.md

---

# Purpose

The Challenge module represents the core learning activity of CipherForge.

A challenge teaches one cybersecurity concept through practical interaction, problem solving, or guided exploration.

Challenges are responsible for presenting learning content.

They are **not responsible for determining correctness**. Evaluation is delegated to the Evaluations module.

---

# Scope

## Included

- Challenge management
- Challenge metadata
- Learning objectives
- Hints
- Learning resources
- Challenge visibility
- Unlock configuration
- Scoring configuration

## Excluded

- Answer validation
- Submission history
- User progress
- Trophy assignment
- Leaderboard calculation

---

# Actors

## Learner

Can:

- View unlocked challenges
- Start challenges
- View hints
- Access learning resources
- Submit answers
- Retry challenges

Cannot:

- Modify challenge content

---

## Administrator

Can:

- Create challenges
- Edit challenges
- Publish challenges
- Hide challenges
- Configure scoring
- Configure evaluation strategy
- Manage hints
- Manage resources

---

# User Stories

## CH-001

As a learner,

I want practical challenges,

So that I can learn by doing.

---

## CH-002

As a learner,

I want hints,

So that I can continue learning when I get stuck.

---

## CH-003

As a learner,

I want learning resources,

So that I can understand the underlying concepts.

---

## CH-004

As an administrator,

I want multiple challenge types,

So that I can teach different cybersecurity skills.

---

## CH-005

As an administrator,

I want to configure how answers are evaluated,

So that different learning activities can use the most appropriate validation method.

---

# Challenge Lifecycle

```
Draft

↓

Review

↓

Published

↓

Hidden

↓

Archived
```

Only **Published** challenges are available to learners.

---

# Challenge Types

Version 1 supports:

## Text Answer

Learner submits text.

Examples:

- Flag
- Command
- Port number
- Hash
- Vulnerability name

---

## AI Conversation

Learner interacts with an AI tutor or simulated target.

Completion is determined by the evaluation engine.

---

## External Website

Learner completes tasks on an external platform.

Evaluation may use an external validator.

---

Future challenge types:

- Docker Lab
- Virtual Machine
- File Analysis
- Packet Analysis
- Source Code Review
- Mobile Application
- Browser Sandbox

---

# Challenge Structure

Every challenge contains:

- Title
- Summary
- Description
- Learning objectives
- Category
- Level
- Estimated duration
- Difficulty indicator
- Visibility status
- Evaluation strategy
- Score value

Optional:

- Hints
- Resources
- Attachments
- External links

---

# Learning Objectives

Every challenge should clearly define:

- What the learner should understand.
- What practical skill should be acquired.
- What prerequisite knowledge is expected.

Learning objectives should be measurable where possible.

---

# Scoring

Each challenge defines:

- Base score
- Hint penalty (optional)
- Retry policy

The scoring algorithm is executed by the Progress module.

Challenges define configuration only.

---

# Hint System

A challenge may have zero or more hints.

Each hint may define:

- Display order
- Penalty
- Unlock condition

Hints should become progressively more specific.

---

# Learning Resources

Resources support learning but do not reveal the answer.

Examples:

- RFCs
- Official documentation
- OWASP pages
- Articles
- Videos

Resources should remain relevant over time.

---

# Retry Policy

Version 1

Unlimited retries.

Future versions may support:

- Attempt limits
- Cooldown periods
- Progressive penalties

---

# Time Limits

Version 1

No mandatory time limit.

Future:

- Timed competitions
- Timed assessments

---

# Visibility

States:

```
Draft

Published

Hidden

Archived
```

Learners only access Published challenges.

---

# Unlock Rules

A challenge may require:

- Previous challenge completion
- Level unlock
- Category completion
- Administrative assignment (future)

Unlock evaluation belongs to the Progress module.

---

# Difficulty

Difficulty is informational.

Suggested values:

- Beginner
- Intermediate
- Advanced
- Expert

Difficulty does not determine unlocking.

---

# Attachments

Optional attachments include:

- ZIP files
- PCAP files
- Images
- PDFs
- Source code
- Logs

Future support:

- Docker images
- VM snapshots

---

# Validation Rules

Title

- Required
- Unique within a level

Description

- Required

Learning objectives

- At least one required

Evaluation strategy

- Required

Score

- Positive integer

---

# Failure Scenarios

Examples:

- Hidden challenge requested.
- Missing evaluation strategy.
- Invalid attachment.
- Learner accesses locked challenge.
- Invalid challenge configuration.

---

# Edge Cases

- Challenge without hints.
- Challenge without resources.
- AI provider unavailable.
- External website offline.
- Attachment removed after publication.

The learner should receive meaningful feedback.

---

# Administrative Operations

Administrators can:

- Clone challenge
- Publish challenge
- Archive challenge
- Preview challenge
- Reorder within level
- Configure scoring
- Configure evaluation
- Manage hints
- Manage resources

All changes should be audited.

---

# API Resources

Base resource

```
/api/v1/challenges
```

Typical operations

```
GET /

GET /{challengeId}

POST /

PATCH /{challengeId}

DELETE /{challengeId}

POST /{challengeId}/publish

POST /{challengeId}/archive
```

Supporting resources

```
/hints

/resources

/attachments
```

Endpoint behavior is defined by the OpenAPI specification.

---

# Data Ownership

Challenges owns:

- Metadata
- Description
- Objectives
- Score configuration
- Hint configuration
- Resource configuration
- Visibility

Evaluations owns:

- Answer validation
- Submission results

Progress owns:

- Completion
- Current score
- Unlock state

---

# Dependencies

Challenges depends on:

- Categories
- Levels

It should not depend directly on:

- Progress
- Leaderboard
- Trophies

---

# Relationships

```
Category

1 ─────────── * Challenge

Level

1 ─────────── * Challenge

Challenge

1 ─────────── * Hint

Challenge

1 ─────────── * Resource

Challenge

1 ─────────── * Attachment
```

---

# Non-Functional Requirements

- Challenge retrieval should be fast.
- Attachments should be served efficiently.
- AI challenge failures should degrade gracefully.
- Challenge metadata should be cacheable.
- Published challenges should be immutable by default unless a new version is created or an administrator explicitly republishes them.

---

# Future Enhancements

Potential additions:

- Docker labs
- VM labs
- Interactive terminals
- Browser-based exploitation
- Multiplayer challenges
- Community challenges
- Adaptive difficulty
- AI-generated hints
- AI-generated walkthroughs
- Peer review challenges

---

# Acceptance Criteria

Challenge Management

- Administrators can create, edit, publish, hide, and archive challenges.

Challenge Presentation

- Learners can access published, unlocked challenges.
- Hints appear in the configured order.
- Resources are available without revealing the solution.

Challenge Configuration

- Every challenge has a defined evaluation strategy.
- Invalid challenge configurations are rejected.

---

# Guiding Principle

A Challenge answers the question:

**"What practical activity will help the learner master this concept?"**

A challenge should teach a single concept well, encourage exploration, and remain independent of how correctness is ultimately evaluated.