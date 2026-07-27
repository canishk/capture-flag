# Category Feature Specification

Version: 1.0

Status: Living Document

Module: Categories

Related Documents

- docs/product/Requirements.md
- docs/architecture/DataModel.md
- docs/architecture/API.md
- docs/features/users.md
- docs/features/authentication.md

---

# Purpose

The Categories module organizes CipherForge learning content into logical subject areas.

Categories provide the first level of navigation for learners and group related levels and challenges under a common topic.

---

# Scope

## Included

- Category management
- Category ordering
- Category visibility
- Category metadata
- Category icons
- Category descriptions

## Excluded

- Difficulty progression
- Challenge management
- Level management
- User progress

---

# Actors

## Learner

Can:

- View available categories
- Browse category information
- View completion status
- View progress within a category

Cannot:

- Create categories
- Edit categories
- Delete categories

---

## Administrator

Can:

- Create categories
- Update categories
- Enable or disable categories
- Reorder categories
- Archive categories (future)

---

# User Stories

## CAT-001

As a learner,

I want to browse available categories,

So that I can choose what I want to learn.

---

## CAT-002

As a learner,

I want to see my progress within each category,

So that I know what to study next.

---

## CAT-003

As an administrator,

I want to create new categories,

So that new learning domains can be introduced.

---

## CAT-004

As an administrator,

I want to disable a category,

So that unfinished or deprecated content is hidden.

---

# Business Rules

A category:

- Represents a learning domain.
- Has a unique name.
- Has one display order.
- Has one icon.
- Has one description.
- Can contain multiple levels.
- Can contain multiple challenges through its levels.

Categories must never represent difficulty.

Examples of valid categories:

- Web Security
- Cryptography
- Linux
- Networking
- Reverse Engineering
- Digital Forensics
- OSINT

Invalid examples:

- Beginner
- Easy
- Hard
- Level 1

Difficulty belongs to the Levels module.

---

# Category Status

Supported states:

```
Active

Hidden

Archived (Future)
```

Hidden categories:

- Cannot be accessed by learners.
- Remain visible to administrators.

---

# Display Order

Categories have an explicit display order.

Learners should see categories according to this order rather than alphabetical sorting unless a different sort option is chosen.

---

# Category Metadata

Each category contains:

- Name
- Description
- Icon
- Display order
- Status

Optional future metadata:

- Banner image
- Color theme
- Estimated completion time
- Recommended prerequisites

---

# Category Completion

A category is considered completed when:

- Every required challenge in every level has been completed.

Completion rules are evaluated by the Progress module.

The Categories module does not calculate progress.

---

# Visibility Rules

Learners:

- See only active categories.

Administrators:

- See all categories.

Future visibility rules may support scheduled publication.

---

# Permissions

## Learner

Can:

- View categories
- View category details

Cannot:

- Modify categories

---

## Administrator

Can:

- Create
- Edit
- Reorder
- Hide
- Restore

Administrative actions should be audited.

---

# Validation Rules

Name

- Required
- Unique
- Minimum length
- Maximum length

Description

- Optional
- Maximum length

Display order

- Integer
- Non-negative

Icon

- Must reference a supported icon identifier or uploaded asset.

---

# Failure Scenarios

Examples:

- Duplicate category name
- Invalid display order
- Hidden category requested by learner
- Unauthorized modification attempt

All failures should return standardized API errors.

---

# Edge Cases

- Reordering multiple categories.
- Disabling a category that contains active levels.
- Category with no levels.
- Category with no challenges.
- Concurrent administrator edits.

---

# Audit Events

Record:

- Category created
- Category updated
- Category hidden
- Category restored
- Display order changed

---

# API Resources

Base resource:

```
/api/v1/categories
```

Typical operations:

```
GET /

GET /{categoryId}

POST /

PATCH /{categoryId}

DELETE /{categoryId}    (administrative archive/disable policy applies)

PATCH /{categoryId}/order
```

Exact endpoint definitions are maintained in the OpenAPI specification.

---

# Data Ownership

Categories owns:

- Name
- Description
- Icon
- Display order
- Status

Progress information is owned by the Progress module.

Levels are owned by the Levels module.

---

# Dependencies

Categories depends only on shared infrastructure.

It should not depend directly on:

- Progress
- Challenges
- Leaderboard

Other modules reference categories through identifiers and service interfaces.

---

# Relationships

```
Category

1 ───────────── * Level
```

Category does not directly own challenge completion or learner progress.

---

# Non-Functional Requirements

- Category listing should be cached where appropriate.
- Category retrieval should support pagination for future scalability.
- Ordering changes should be transactional.
- Hidden categories must never appear in learner-facing APIs.

---

# Future Enhancements

Potential additions:

- Nested categories
- Learning paths
- Category prerequisites
- Category difficulty indicators
- Localization
- Community-created categories
- Featured categories
- Seasonal categories

These enhancements should preserve the existing category identity.

---

# Acceptance Criteria

Category Listing

- Learners see only active categories.
- Categories appear in configured display order.

Category Management

- Administrators can create categories.
- Duplicate names are rejected.
- Categories can be updated.
- Categories can be hidden and restored.

Navigation

- A category can contain multiple levels.
- Categories without levels are still valid but should be identifiable as incomplete content.

---

# Guiding Principle

A Category answers the question:

**"What subject am I learning?"**

It should organize content into clear, stable learning domains while remaining independent of learner progress, challenge difficulty, and completion logic.