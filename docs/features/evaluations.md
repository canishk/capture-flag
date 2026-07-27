# Evaluation Feature Specification

Version: 1.0

Status: Living Document

Module: Evaluations

Related Documents

- docs/features/challenges.md
- docs/features/submissions.md
- docs/features/progress.md
- docs/architecture/EventModel.md
- docs/architecture/API.md
- docs/architecture/Security.md

---

# Purpose

The Evaluations module determines whether a learner's submission satisfies the completion criteria for a challenge.

It is responsible only for evaluating submissions.

It does not own:

- Challenges
- Progress
- Scores
- Leaderboards
- Trophies

Evaluation produces an outcome that other modules consume.

---

# Scope

## Included

- Evaluation strategies
- Submission validation
- Result generation
- Evaluation feedback
- AI-assisted evaluation
- External validators
- Evaluation configuration

## Excluded

- Submission history
- Challenge presentation
- Learning progress
- Scoring
- Unlocking
- Trophy assignment

---

# Design Principles

The Evaluations module follows these principles:

- Strategy Pattern
- Deterministic when possible
- Extensible
- Auditable
- Repeatable
- Secure by Default

Every evaluation strategy implements a common interface.

---

# Actors

## Learner

Can:

- Submit answers
- Receive evaluation results
- View feedback

Cannot:

- Choose evaluation strategy
- Access evaluation configuration

---

## Administrator

Can:

- Select evaluation strategy
- Configure strategy parameters
- Preview evaluations
- Test evaluation rules

---

# User Stories

## EVAL-001

As a learner,

I want immediate feedback,

So that I know whether my answer is correct.

---

## EVAL-002

As a learner,

I want meaningful feedback,

So that I can improve without being given the solution.

---

## EVAL-003

As an administrator,

I want multiple evaluation strategies,

So that different challenge types can be supported.

---

## EVAL-004

As an administrator,

I want to test an evaluation configuration,

So that I can verify challenge behavior before publication.

---

# Evaluation Lifecycle

```
Submission Created

↓

Input Validation

↓

Strategy Selection

↓

Evaluation

↓

Result Generated

↓

Domain Event Published
```

---

# Evaluation Result

Every evaluation produces one result.

Possible outcomes:

```
Passed

Failed

Partially Passed (Future)

Error

Pending (Future)
```

---

# Evaluation Strategies

Version 1 supports:

## Exact Match

Submission must exactly equal the expected answer.

Examples:

- Flags
- Commands
- CVE identifiers

---

## Regular Expression

Submission matches a configured regular expression.

Examples:

- Hash formats
- IPv4 addresses
- Email formats

---

## Numeric Range

Submission falls within a defined range.

Examples:

- Port numbers
- Scores
- Time values

---

## Cosine Similarity

Semantic comparison of learner text against one or more reference answers.

Examples:

- Explain SQL Injection
- Describe CIA Triad
- Explain least privilege

Administrator configures:

- Embedding model
- Similarity threshold

---

## AI Judge

An LLM evaluates the submission using configurable instructions.

Examples:

- Explain exploitation steps
- Analyze a vulnerability
- Produce secure code

AI evaluation should return structured output.

---

## External Validator

Evaluation is delegated to another service.

Examples:

- External lab
- Sandbox
- CTF engine
- Third-party platform

---

# Strategy Configuration

Each strategy owns its own configuration.

Examples:

Exact Match

```
expectedAnswer
caseSensitive
trimWhitespace
```

Regex

```
pattern
flags
```

Cosine Similarity

```
referenceAnswers

embeddingModel

threshold
```

AI Judge

```
systemPrompt

rubric

minimumScore
```

---

# Feedback

Feedback should help learning without revealing the answer.

Examples:

Good:

```
Incorrect.

Review how SQL injection bypasses authentication.
```

Poor:

```
Correct answer:

' OR 1=1 --
```

---

# Evaluation Events

The module publishes:

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

# Validation Rules

Every evaluation configuration must define:

- Strategy
- Required parameters
- Valid configuration values

Invalid configurations cannot be published.

---

# AI Evaluation Principles

AI evaluation must:

- Use structured prompts.
- Return structured responses.
- Produce deterministic output where practical.
- Log evaluation metadata.
- Never expose internal prompts.

Administrator-defined rubrics should drive scoring.

---

# External Validators

External validation should support:

- Timeout
- Retry
- Authentication
- Health checks
- Versioning

Failures should return controlled error responses.

---

# Failure Scenarios

Examples:

- Unsupported strategy
- Missing configuration
- AI provider unavailable
- Validator timeout
- Invalid submission format

Failures should never corrupt learner progress.

---

# Security

Evaluation must:

- Validate all inputs.
- Sanitize AI prompts.
- Protect API keys.
- Prevent prompt injection where practical.
- Avoid executing learner input directly.

Evaluation services should never expose secrets.

---

# Performance

Expected targets:

- Exact Match < 50 ms
- Regex < 50 ms
- Numeric Range < 50 ms
- Cosine Similarity < 500 ms
- AI Judge < configurable timeout
- External Validator < configurable timeout

Long-running evaluations should execute asynchronously.

---

# Audit Events

Record:

- Strategy selected
- Evaluation completed
- Evaluation failed
- Configuration updated

Audit records must never include sensitive data.

---

# API Resources

Base resource:

```
/api/v1/evaluations
```

Typical operations:

```
POST /evaluate

GET /strategies

GET /strategies/{strategy}

POST /preview

POST /validate-config
```

Challenge-specific configuration:

```
GET /challenges/{challengeId}/evaluation

PATCH /challenges/{challengeId}/evaluation
```

OpenAPI defines the canonical contract.

---

# Data Ownership

Evaluations owns:

- Strategy
- Strategy configuration
- Evaluation result
- Feedback
- Evaluation metadata

Submissions owns:

- Learner answer
- Attempt history

Progress owns:

- Completion
- Score
- Unlock state

---

# Dependencies

Evaluations depends on:

- Challenges
- Submissions

It should not depend directly on:

- Progress
- Leaderboard
- Trophies

Those modules subscribe to evaluation events.

---

# Relationships

```
Challenge

1 ─────────── 1 Evaluation Strategy

Submission

1 ─────────── 1 Evaluation Result
```

Future versions may support composite evaluation strategies.

---

# Non-Functional Requirements

- Evaluation strategies must be independently testable.
- Strategy execution should be deterministic whenever possible.
- AI evaluations should include observability metrics.
- External validator failures should degrade gracefully.
- New strategies should be added without modifying existing implementations.

---

# Future Enhancements

Potential additions:

- Composite strategies
- Weighted scoring rubrics
- Multi-stage evaluation
- Human review workflow
- Plagiarism detection
- Peer review
- Custom strategy plugins
- Code execution sandbox
- Docker-based validation
- Kubernetes lab validation

---

# Acceptance Criteria

Evaluation

- Every challenge has exactly one evaluation strategy in Version 1.
- Valid submissions receive an evaluation result.
- Invalid configurations cannot be published.

Feedback

- Learners receive meaningful feedback.
- Feedback never reveals protected answers.

Administration

- Administrators can configure and preview evaluation strategies.
- Strategies validate configuration before publication.

---

# Guiding Principle

An Evaluation answers the question:

**"Did the learner demonstrate the required understanding or skill?"**

Evaluation should remain independent of challenge presentation and learner progression, allowing CipherForge to evolve new validation techniques without redesigning the learning experience.