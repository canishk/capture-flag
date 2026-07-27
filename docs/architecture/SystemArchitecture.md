# System Architecture

Version: 1.0

Status: Living Document

Document: SystemArchitecture.md

---

# Purpose

This document describes the overall architecture of CipherForge.

It defines:

- System boundaries
- Architectural principles
- Module responsibilities
- Communication patterns
- Deployment topology
- Infrastructure
- Data ownership
- Event processing
- Scalability strategy

All implementation decisions should align with this document.

---

# Architectural Style

CipherForge is built as a **Modular Monolith** with clear module boundaries.

Characteristics:

- Single deployable application
- Independent business modules
- Shared infrastructure
- Event-driven communication
- CQRS-inspired read/write separation

The architecture intentionally avoids microservices until operational complexity justifies decomposition.

---

# System Goals

The architecture prioritizes:

- Simplicity
- Maintainability
- Scalability
- Testability
- Security
- Observability
- AI-assisted development

---

# High-Level Architecture

```
                    Web Browser
                         │
                         ▼
                Next.js Frontend
                         │
                    HTTPS / REST
                         │
                         ▼
                  FastAPI Backend
                         │
 ┌──────────────────────────────────────────┐
 │                                          │
 │ Authentication                           │
 │ Users                                    │
 │ Challenges                               │
 │ Categories                               │
 │ Levels                                   │
 │ Hints                                    │
 │ Resources                                │
 │ Submissions                              │
 │ Evaluations                              │
 │ Progress                                 │
 │ Trophies                                 │
 │ Leaderboards                             │
 │ Analytics                                │
 │ Notifications                            │
 │                                          │
 └──────────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
     PostgreSQL                     Redis
```

---

# Technology Stack

## Frontend

- Next.js
- TypeScript
- React
- Tailwind CSS
- TanStack Query
- React Hook Form

---

## Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic
- Alembic

---

## Database

PostgreSQL

Primary transactional datastore.

---

## Cache

Redis

Used for:

- caching
- background jobs
- rate limiting
- session storage (optional)
- distributed locks

---

## Background Processing

Worker process using Redis-backed queues.

Responsible for:

- notification delivery
- analytics aggregation
- projection updates
- scheduled jobs
- future AI tasks

---

# Architectural Principles

## Business Modules

Every business capability owns:

- API
- Service layer
- Domain logic
- Repository
- Events
- Tests

Modules communicate through interfaces and domain events.

---

## Single Responsibility

Every module owns one business capability.

Examples:

Users

owns profiles.

Evaluations

owns answer validation.

Progress

owns learner state.

---

## Data Ownership

Each table has one owner.

Only the owning module may modify its tables.

Other modules consume:

- APIs
- Events
- Read models

Never direct writes.

---

## Event-Driven Communication

Modules publish events instead of calling each other whenever practical.

Example:

```
SubmissionCreated

↓

Evaluation

↓

SubmissionEvaluated

↓

ProgressUpdated

↓

LeaderboardUpdated
```

---

## CQRS-Inspired Design

Write Side

```
Users

Challenges

Submissions

Evaluations
```

Read Side

```
Progress

Leaderboards

Analytics

Notifications
```

Read models are rebuildable.

---

# Module Map

Core Learning

```
Authentication

Users

Categories

Levels

Challenges

Hints

Resources
```

Learning Workflow

```
Submissions

Evaluations

Progress
```

Recognition

```
Trophies

Leaderboards
```

Insights

```
Analytics
```

Communication

```
Notifications
```

Infrastructure

```
Projection Engine

Rule Engine

Notification Engine

Event Dispatcher
```

---

# Request Lifecycle

```
Browser

↓

REST API

↓

FastAPI Router

↓

Application Service

↓

Domain Logic

↓

Repository

↓

Database

↓

Publish Domain Events

↓

Background Workers

↓

Read Model Updates

↓

Notification Delivery
```

---

# Module Structure

Recommended structure:

```
modules/

authentication/

users/

categories/

levels/

challenges/

hints/

resources/

submissions/

evaluations/

progress/

trophies/

leaderboards/

analytics/

notifications/
```

Every module contains:

```
api/

application/

domain/

infrastructure/

schemas/

repositories/

events/

tests/
```

---

# Infrastructure Modules

Shared infrastructure:

```
database/

cache/

events/

messaging/

security/

logging/

configuration/

storage/
```

Infrastructure contains no business rules.

---

# Event Processing

```
Business Module

↓

Domain Event

↓

Event Dispatcher

↓

Projection Engine

↓

Rule Engine

↓

Notification Engine
```

Each processor is independent.

---

# Projection Engine

Responsible for:

- Progress
- Leaderboards
- Analytics

Characteristics:

- rebuildable
- deterministic
- idempotent

---

# Rule Engine

Evaluates:

- trophies
- unlock rules
- recommendations
- future automation

Rules are declarative.

---

# Notification Engine

Responsible for:

- template rendering
- preference checks
- channel routing
- retry handling

Delivery channels are plugins.

---

# Data Flow

Write

```
Submission

↓

Evaluation

↓

Events
```

Read

```
Events

↓

Progress

↓

Leaderboards

↓

Analytics
```

---

# Database Ownership

Authentication

- credentials
- sessions

Users

- profiles

Challenges

- challenge metadata

Hints

- hint records

Resources

- resource records

Submissions

- learner attempts

Evaluations

- evaluation results

Progress

- projections

Leaderboards

- rankings

Notifications

- notification history

Analytics

- aggregates

---

# API Design

REST APIs

```
/api/v1/
```

Examples:

```
/users

/challenges

/submissions

/progress

/leaderboards
```

Every module owns its endpoints.

---

# Security Boundaries

Authentication

- identity

Authorization

- permissions

Business Modules

- business rules

Infrastructure

- transport security

---

# Authentication Flow

```
Login

↓

JWT

↓

API

↓

Authorization

↓

Business Module
```

---

# Authorization

Authorization is policy-based.

Avoid hardcoded role checks inside business logic.

Future support:

- permissions
- scopes
- feature flags

---

# Configuration

Configuration stored in:

```
.env

application.yaml
```

Secrets never exist in source control.

---

# Observability

Logging

- structured

Metrics

- Prometheus compatible

Tracing

- OpenTelemetry ready

Health Checks

```
/health

/ready

/live
```

---

# Background Jobs

Examples:

- leaderboard rebuild
- analytics aggregation
- email delivery
- cleanup jobs
- scheduled maintenance

Jobs are retryable.

---

# Caching Strategy

Redis caches:

- challenge metadata
- categories
- resources
- leaderboard pages

Never cache mutable transactional writes.

---

# File Storage

Future abstraction:

```
Storage Provider

↓

Local

S3

Azure Blob

Google Cloud Storage
```

Business modules remain storage agnostic.

---

# Deployment

Version 1

```
Docker Compose

↓

NGINX

↓

FastAPI

↓

Worker

↓

PostgreSQL

↓

Redis
```

---

Future

```
Kubernetes

↓

Horizontal Scaling

↓

Managed PostgreSQL

↓

Managed Redis
```

---

# Scalability Strategy

Phase 1

Single instance.

Phase 2

Multiple API instances.

Phase 3

Separate worker pool.

Phase 4

Dedicated read replicas.

Phase 5

Optional microservice extraction.

Modules remain independently extractable.

---

# Failure Isolation

Failures should remain localized.

Examples:

Notification failure

↓

Business transaction succeeds.

Analytics failure

↓

Learner experience unaffected.

Leaderboard rebuild

↓

Progress unaffected.

---

# Disaster Recovery

Backups

- PostgreSQL
- configuration
- uploaded files

Recovery

- restore database
- replay projections
- verify consistency

---

# Testing Strategy

Unit Tests

Business rules.

Integration Tests

Module boundaries.

Contract Tests

API behavior.

End-to-End Tests

Complete learner workflows.

---

# AI-Assisted Development

The architecture is optimized for AI tooling.

Characteristics:

- Stable module boundaries
- Small files
- Clear ownership
- Explicit interfaces
- Documentation-first workflow

Each module should be understandable independently.

---

# Future Evolution

Potential additions:

- AI Tutor
- Learning Paths
- Organizations
- Teams
- Multiplayer competitions
- External integrations
- Plugin framework
- Marketplace

These should integrate through domain events and module interfaces rather than modifying existing modules.

---

# Architecture Decision Record (ADR)

Significant architectural changes should be captured as ADRs.

Recommended structure:

```
docs/adr/

ADR-0001-Modular-Monolith.md

ADR-0002-Event-Driven-Architecture.md

ADR-0003-CQRS-Projections.md
```

ADRs explain *why* a decision was made, complementing this document's description of *how* the system is structured.

---

# Guiding Principles

1. Every business capability has one owner.
2. Every table has one owner.
3. Domain events communicate between modules.
4. Read models are projections, not sources of truth.
5. Infrastructure supports business modules, never contains business rules.
6. Favor simplicity over premature distribution.
7. Design today so modules can be extracted tomorrow.