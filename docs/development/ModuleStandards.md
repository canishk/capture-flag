# Module Standards

Version: 1.0

Status: Living Document

Related Documents

- Architecture/Overview.md
- Architecture/Backend.md
- Development/CodingStandards.md

---

# Purpose

This document defines the standard structure, responsibilities, and development rules for every backend module in CipherForge.

Every module should look familiar to a developer who has worked on any other module.

Consistency is considered more important than cleverness.

---

# What is a Module?

A module is an independent business domain.

Examples:

- Authentication
- Users
- Categories
- Levels
- Challenges
- Progress
- Evaluations
- AI
- Leaderboard
- Trophies
- Administration

Each module owns its business logic and persistence.

---

# Module Principles

Every module should:

- Have a single responsibility.
- Own its own business logic.
- Be independently testable.
- Be loosely coupled.
- Minimize dependencies on other modules.

---

# Standard Directory Layout

Every module follows the same structure.

```
module_name/

    __init__.py

    router.py
    service.py
    repository.py

    models.py
    schemas.py

    validators.py
    exceptions.py

    constants.py

    dependencies.py

    interfaces.py

    mapper.py

    permissions.py

    events.py

    README.md
```

Not every file is required immediately.

However, file names should remain consistent across modules.

---

# Required Files

Every module must contain at minimum:

```
router.py

service.py

repository.py

schemas.py
```

Persistence modules additionally require:

```
models.py
```

---

# Optional Files

Add only when required.

```
validators.py

permissions.py

mapper.py

events.py

constants.py

exceptions.py

interfaces.py
```

Do not create empty files.

---

# Responsibilities

## Router

Responsible for:

- HTTP routes
- Request parsing
- Authentication
- Response formatting

Must never contain:

- SQL
- Business rules
- Complex validation

---

## Service

Responsible for:

- Business logic
- Use cases
- Orchestration
- Transactions

Services are the heart of every module.

---

## Repository

Responsible for:

- CRUD
- Queries
- Persistence

Repositories never decide business behavior.

---

## Models

Represent persistent entities.

Models should remain lightweight.

Avoid business logic.

---

## Schemas

Represent API contracts.

Use Pydantic models only.

Never expose ORM models directly.

---

## Validators

Contains reusable business validations.

Example

```
validate_progress()

validate_level_unlock()
```

---

## Permissions

Contains reusable authorization rules.

Example

```
can_edit_category()

can_delete_challenge()
```

---

## Mapper

Responsible for converting between:

- ORM models
- DTOs
- API responses

Avoid mixing mapping logic into services.

---

## Constants

Contains module-specific constants.

Do not place magic values throughout the code.

---

## Events

Future extension point.

Examples

ChallengeCompleted

UserRegistered

TrophyUnlocked

Version 1 may leave this empty.

---

# Dependency Rules

Allowed

```
Router

↓

Service

↓

Repository

↓

Database
```

Forbidden

```
Router → Repository

Router → Database

Repository → Router

Repository → Service
```

---

# Cross Module Communication

Modules communicate through services.

Example

```
ChallengeService

↓

ProgressService

↓

TrophyService
```

Never call another module's repository directly.

Never manipulate another module's models.

---

# Public Interface

Every module should expose a minimal public interface.

External modules should not know internal implementation details.

---

# Naming Conventions

Services

```
ChallengeService

ProgressService
```

Repositories

```
ChallengeRepository

UserRepository
```

Schemas

```
ChallengeCreateRequest

ChallengeUpdateRequest

ChallengeResponse
```

Models

```
Challenge

Category
```

---

# Business Rules

Business rules belong only in services.

Never place business logic in:

- Routers
- Repositories
- Models
- Schemas

---

# Transactions

Transactions should be initiated by services.

Repositories should not manage transactions independently.

---

# Validation Strategy

Validation happens in three layers.

API

↓

Business

↓

Database

Each layer validates different concerns.

Avoid duplicated validation.

---

# Error Handling

Each module defines domain-specific exceptions.

Example

```
ChallengeNotFound

DuplicateCategory

InvalidProgress
```

Do not expose infrastructure exceptions directly.

---

# Logging

Every module should log:

- Significant business events
- Warnings
- Unexpected failures

Avoid excessive logging.

Never log secrets.

---

# Testing

Each module should have corresponding tests.

Recommended structure

```
tests/

    module_name/

        test_router.py

        test_service.py

        test_repository.py
```

Business logic should be testable without HTTP.

---

# Documentation

Every module should include:

README.md

The README should describe:

- Purpose
- Responsibilities
- Public APIs
- Dependencies

Keep documentation concise.

---

# Module Independence

Whenever possible:

A module should be understandable without reading unrelated modules.

Dependencies should remain explicit.

---

# Module Lifecycle

Typical lifecycle:

```
Requirement

↓

Story

↓

Module Implementation

↓

Testing

↓

Documentation

↓

Review

↓

Release
```

---

# Future Growth

As modules become larger, they may introduce additional files.

Example

```
services/

repositories/

schemas/

validators/
```

Do not introduce subdirectories until complexity justifies them.

---

# Anti-Patterns

Avoid:

- God Services
- Utility classes with unrelated functions
- Circular dependencies
- Duplicate validation
- Direct database access from routers
- Cross-module repository access
- Business logic inside ORM models
- Business logic inside API schemas

---

# Definition of a Healthy Module

A healthy module is one that:

- Has a single responsibility.
- Is independently testable.
- Is loosely coupled.
- Is easy to understand.
- Has minimal public surface area.
- Can evolve without impacting unrelated modules.

When creating a new module, use this document as the implementation standard.