# Data Model

Version: 1.0

Status: Living Document

Related Documents

- docs/product/Requirements.md
- docs/architecture/Overview.md
- docs/architecture/Database.md
- docs/architecture/ModuleStandards.md

---

# Purpose

This document defines the business data model of CipherForge.

It identifies the core business entities, their responsibilities, ownership, and relationships.

This document is intentionally technology-agnostic. It describes the business domain rather than SQL implementation details.

---

# Domain Overview

CipherForge consists of the following business domains:

```
Authentication

↓

Users

↓

Learning Content

↓

Challenge Engine

↓

Progress Tracking

↓

Achievements

↓

Analytics

↓

Administration
```

Each domain owns its own data and business rules.

---

# High-Level Entity Relationship

```
User
 │
 ├──────────────┐
 │              │
 │              │
Progress     Submission
 │              │
 │              │
Level       Challenge
 │              │
 │              │
Category───────┘
 │
 └──────── Trophy

User
 │
 └──────── LeaderboardEntry

Challenge
 │
 ├──────── Hint
 │
 ├──────── Resource
 │
 └──────── AIConversation
```

---

# Entity Catalogue

## User

### Module

Users

### Purpose

Represents a learner or administrator.

### Responsibilities

- Authentication identity
- Profile
- Preferences
- Learning ownership

### Relationships

```
User

1 ──────── * Progress

1 ──────── * Submission

1 ──────── * Trophy

1 ──────── * LeaderboardEntry
```

---

## Category

### Module

Categories

### Purpose

Top-level learning area.

Examples:

- Web Security
- Cryptography
- Networking
- Linux
- Reverse Engineering

### Relationships

```
Category

1 ──────── * Level

1 ──────── * Challenge
```

---

## Level

### Module

Levels

### Purpose

Represents learning progression inside a category.

Example

```
Beginner

Intermediate

Advanced

Expert
```

### Relationships

```
Category

1 ──────── * Level

Level

1 ──────── * Challenge
```

---

## Challenge

### Module

Challenges

### Purpose

Represents an exercise that teaches one concept.

### Supported Types

- Text Answer
- AI Conversation
- External Website

Future

- Docker Lab
- VM Lab
- Mobile App
- File Analysis

### Relationships

```
Challenge

* ──────── 1 Level

* ──────── 1 Category

1 ──────── * Hint

1 ──────── * Resource

1 ──────── * Submission
```

---

## Submission

### Module

Evaluations

### Purpose

Stores every learner attempt.

### Responsibilities

- Submitted answer
- Evaluation result
- Timestamp
- Score

### Relationships

```
User

1 ──────── * Submission

Challenge

1 ──────── * Submission
```

---

## Progress

### Module

Progress

### Purpose

Represents overall learner progression.

### Responsibilities

- Current level
- Completion status
- Unlocks

### Relationships

```
User

1 ──────── * Progress

Challenge

1 ──────── * Progress
```

---

## Trophy

### Module

Trophies

### Purpose

Represents achievements earned by learners.

Examples

```
First Challenge

100 Points

Perfect Week

Linux Explorer
```

### Relationships

```
User

1 ──────── * Trophy
```

---

## LeaderboardEntry

### Module

Leaderboard

### Purpose

Represents ranking information.

Stores:

- Points
- Rank
- Completed challenges

Leaderboard generation rules are handled by the service layer.

---

## Hint

### Module

Challenges

### Purpose

Optional guidance for solving a challenge.

Hints may:

- Reduce score
- Require previous attempts

Business rules belong to services.

---

## Resource

### Module

Challenges

### Purpose

Learning references.

Examples

- Documentation
- RFCs
- Videos
- Articles

Resources support learning rather than evaluation.

---

## AIConversation

### Module

AI

### Purpose

Stores conversations for AI-based challenges.

Contains:

- Prompt history
- Evaluation metadata
- Completion state

Conversation logic belongs to the AI module.

---

# Ownership Matrix

| Entity | Owning Module |
|---------|---------------|
| User | Users |
| Category | Categories |
| Level | Levels |
| Challenge | Challenges |
| Submission | Evaluations |
| Progress | Progress |
| Trophy | Trophies |
| LeaderboardEntry | Leaderboard |
| Hint | Challenges |
| Resource | Challenges |
| AIConversation | AI |

Only the owning module may directly modify its entities.

---

# Relationship Rules

## User → Progress

One user has many progress records.

---

## User → Submission

Every submission belongs to exactly one user.

---

## Challenge → Submission

Every challenge has many submissions.

---

## Category → Level

One category contains multiple levels.

---

## Level → Challenge

One level contains multiple challenges.

---

## Challenge → Hint

A challenge may contain zero or more hints.

---

## Challenge → Resource

A challenge may include zero or more learning resources.

---

## User → Trophy

A learner may earn many trophies.

---

## User → LeaderboardEntry

Leaderboard entries are derived from user activity.

---

# Derived Data

Some information should be calculated rather than permanently stored.

Examples:

- Current rank
- Completion percentage
- Total score
- Success rate

Materialized views or caches may be introduced later if required.

---

# Domain Events

The following business events may occur:

```
UserRegistered

ChallengeStarted

ChallengeCompleted

ChallengeFailed

HintViewed

LevelUnlocked

CategoryCompleted

TrophyAwarded

LeaderboardUpdated
```

Version 1 does not require event sourcing.

These events represent important business actions.

---

# Aggregate Boundaries

Suggested aggregates:

```
User
 ├── Progress
 ├── Trophy
 └── Submission

Category
 ├── Level
 └── Challenge

Challenge
 ├── Hint
 ├── Resource
 └── AIConversation
```

Aggregates define consistency boundaries for business operations.

---

# Future Entities

The following entities are intentionally excluded from Version 1 but anticipated in future releases:

- Team
- Organization
- Competition
- Plugin
- MarketplaceItem
- DockerLab
- VirtualMachine
- Certificate
- Course
- LearningPath
- BadgeCollection

Their absence should not influence current design decisions.

---

# Design Principles

Every entity should:

- Represent one business concept.
- Have a single owner.
- Avoid duplication of responsibility.
- Support future extensibility.
- Remain independent of framework implementation.

---

# Guiding Principle

The data model reflects the business domain, not the application's current implementation.

Business concepts should remain stable even as technology, frameworks, and storage evolve.