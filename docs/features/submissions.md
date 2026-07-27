# Submission Feature Specification

Version: 1.0

Status: Living Document

Module: Submissions

Related Documents

- docs/features/challenges.md
- docs/features/evaluations.md
- docs/features/progress.md
- docs/architecture/EventModel.md
- docs/architecture/DataModel.md
- docs/architecture/API.md

---

# Purpose

The Submissions module records every learner attempt to complete a challenge.

A submission represents an immutable snapshot of:

- The learner's answer
- The challenge being attempted
- The evaluation request
- The evaluation outcome

Submissions provide the historical record of learning activity.

---

# Scope

## Included

- Submission creation
- Submission history
- Attempt tracking
- Submission metadata
- Submission status
- Evaluation requests
- Submission retrieval

## Excluded

- Answer validation
- Progress calculation
- Trophy assignment
- Leaderboard updates
- Challenge presentation

---

# Design Principles

The module follows these principles:

- Immutable records
- Append-only history
- Full auditability
- Event-driven integration
- Independent of evaluation logic

A submission is never modified after creation.

---

# Actors

## Learner

Can:

- Submit answers
- View personal submission history
- View evaluation outcomes
- Retry challenges

Cannot:

- Modify previous submissions
- Delete submissions
- View submissions from other learners

---

## Administrator

Can:

- View all submissions
- Search submissions
- Filter submissions
- Export submissions (future)

Cannot:

- Modify learner submissions

---

# User Stories

## SUB-001

As a learner,

I want every attempt recorded,

So that I can track my improvement.

---

## SUB-002

As a learner,

I want to retry a challenge,

So that I can continue learning.

---

## SUB-003

As an administrator,

I want to inspect submission history,

So that I can troubleshoot challenges and investigate issues.

---

## SUB-004

As an administrator,

I want submission statistics,

So that I can improve challenge quality.

---

# Submission Lifecycle

```
Created

↓

Queued (Future)

↓

Evaluating

↓

Completed
```

Possible terminal states:

```
Passed

Failed

Error

Cancelled (Future)
```

---

# Submission Ownership

Every submission belongs to exactly:

- One learner
- One challenge

A learner may create many submissions for the same challenge.

---

# Submission Contents

Each submission contains:

- Submission ID
- User ID
- Challenge ID
- Evaluation Strategy
- Submitted Answer
- Submitted At
- Attempt Number
- Evaluation Status
- Evaluation Result
- Feedback
- Processing Time

Optional metadata:

- Client version
- Device type
- IP address (configurable)
- Correlation ID

---

# Attempt Number

Attempt numbers are sequential per learner and challenge.

Example:

```
Challenge 42

Attempt 1

Attempt 2

Attempt 3
```

Attempt numbers must never be reused.

---

# Submission Status

Supported statuses:

```
Pending

Evaluating

Completed

Failed

Error
```

Pending and Evaluating support asynchronous strategies.

---

# Retry Policy

Version 1

Unlimited submissions.

Future options:

- Maximum attempts
- Cooldown periods
- Daily limits
- Instructor overrides

Retry policy belongs to the Challenge configuration.

---

# Evaluation Flow

```
Submission Created

↓

SubmissionCreated Event

↓

Evaluation Module

↓

Evaluation Result

↓

Submission Updated

↓

SubmissionEvaluated Event
```

Only the evaluation outcome is updated after creation.

The original submitted answer remains immutable.

---

# Submission History

Learners can view:

- Submission timestamp
- Attempt number
- Pass/fail result
- Feedback
- Processing duration

Learners cannot view:

- Other users' submissions
- Internal evaluation configuration

---

# Administrative Search

Administrators should be able to filter by:

- User
- Challenge
- Category
- Level
- Status
- Evaluation strategy
- Date range

Future filters:

- AI provider
- Similarity score
- Processing duration

---

# Validation Rules

Submission must:

- Reference an existing challenge
- Belong to an authenticated learner
- Contain a supported answer format

Rejected submissions are not stored.

---

# Failure Scenarios

Examples:

- Challenge archived
- Challenge locked
- Invalid answer format
- Evaluation timeout
- External validator unavailable
- AI provider unavailable

Failures should create diagnostic logs.

---

# Edge Cases

- Duplicate submission requests
- Browser refresh during evaluation
- Network interruption after submission
- Long-running AI evaluation
- External validator timeout

Duplicate requests should be detected through idempotency mechanisms where appropriate.

---

# Events

The module publishes:

```
SubmissionCreated
```

The Evaluations module publishes:

```
SubmissionEvaluated

EvaluationPassed

EvaluationFailed
```

Subscribers include:

- Progress
- Analytics
- Notifications

---

# Security

Learners may access only their own submissions.

Administrators require elevated permissions.

Sensitive submission content should:

- Never appear in logs
- Never expose evaluation secrets
- Be sanitized before AI evaluation

---

# Privacy

Submission history belongs to the learner.

Future versions may support:

- Data retention policies
- Export requests
- Account deletion workflows
- Anonymization

---

# Audit

Record:

- Submission created
- Evaluation started
- Evaluation completed
- Evaluation failed

Audit logs are separate from submission history.

---

# API Resources

Base resource:

```
/api/v1/submissions
```

Typical operations:

```
POST /

GET /{submissionId}

GET /me

GET /challenge/{challengeId}

GET /
```

Administrative endpoints:

```
GET /search

GET /statistics
```

The OpenAPI specification is the authoritative API definition.

---

# Data Ownership

Submissions owns:

- Learner answer
- Attempt number
- Submission metadata
- Submission status
- Evaluation reference

Evaluations owns:

- Evaluation logic
- Evaluation configuration
- Evaluation feedback

Progress owns:

- Completion
- Current score
- Unlock state

---

# Dependencies

Submissions depends on:

- Challenges
- Users

It communicates with Evaluations through domain events.

It must not depend on:

- Progress
- Leaderboard
- Trophies

---

# Relationships

```
User

1 ───────────── * Submission

Challenge

1 ───────────── * Submission

Submission

1 ───────────── 1 Evaluation Result
```

A submission belongs to one challenge and one learner.

---

# Non-Functional Requirements

- Submission creation should be reliable and transactional.
- Submission history should support efficient pagination.
- Long-running evaluations should not block submission creation.
- Large submission volumes should remain queryable through indexing.
- Submission identifiers should be globally unique.

---

# Future Enhancements

Potential additions:

- Draft submissions
- Offline submission queue
- Batch submissions
- File uploads
- Code submissions
- Digital signatures
- Replay evaluations
- Submission comparison
- AI-assisted submission review

---

# Acceptance Criteria

Submission

- Every learner submission creates a new immutable record.
- Attempt numbers increment correctly.
- Submission history is preserved.

Evaluation

- Each submission triggers exactly one evaluation request.
- Evaluation outcomes are linked to the submission.

Security

- Learners cannot access another learner's submissions.
- Administrators can search and filter submissions.
- Sensitive submission data is protected.

---

# Guiding Principle

A Submission answers the question:

**"What did the learner submit at this moment in time?"**

It represents an immutable historical record of a learning attempt. Progress may change over time, evaluation strategies may evolve, and scoring rules may be updated—but a submission should always preserve exactly what the learner submitted and when they submitted it.