# Coding Standards

Version: 1.0

---

## Purpose

This document defines the engineering standards for the CipherForge project.

Every contributor is expected to follow these standards.

---

# General Principles

* Prefer readability over cleverness.
* Write code for humans first.
* Keep modules cohesive.
* Keep functions focused.
* Avoid premature optimization.
* Prefer explicit behavior over implicit behavior.

---

# Naming Conventions

## Files

* snake_case for Python files
* PascalCase for React components

Examples

```
challenge_service.py
challenge_repository.py

ChallengeCard.tsx
LoginForm.tsx
```

---

## Variables

Use descriptive names.

Good

```
completed_challenges
current_level
challenge_points
```

Avoid

```
tmp
obj
val
data
```

---

## Functions

Functions should:

* Have one responsibility.
* Return one logical result.
* Be short enough to understand without scrolling.

---

## Classes

Classes should model one concept.

Avoid "utility" classes containing unrelated functions.

---

# Backend Rules

Architecture

```
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Rules

* Routers contain HTTP logic only.
* Services contain business rules.
* Repositories access persistence only.
* Models represent persisted entities.
* Schemas validate input/output.

---

# Frontend Rules

* Components render UI.
* Hooks manage behavior.
* API calls are centralized.
* Avoid duplicated state.
* Prefer composition over inheritance.

---

# Error Handling

* Raise domain-specific exceptions.
* Never suppress exceptions silently.
* Return meaningful API errors.
* Log unexpected failures.

---

# Logging

Use structured logging.

Never use:

```
print()
```

Never log:

* Passwords
* Tokens
* Secrets
* Personal information

---

# Documentation

Document:

* Public classes
* Public functions
* Complex algorithms

Explain *why*, not *what*.

---

# Type Safety

Python

* Type hints are mandatory.

TypeScript

* Avoid `any`.
* Prefer strict typing.

---

# Formatting

Python

* Ruff
* Black-compatible formatting

TypeScript

* ESLint
* Prettier

---

# Testing

Every business rule should be testable.

Prefer:

* Unit tests
* Integration tests

Avoid testing implementation details.

---

# Code Reviews

Every change should improve one or more of:

* Readability
* Maintainability
* Correctness
* Testability

---

# File: docs/development/ProjectStructure.md

# Project Structure

Version: 1.0

---

# Repository

```
CipherForge/

backend/
frontend/
docs/
docker/
scripts/
.github/
.cursor/
```

---

# Backend

```
backend/

app/
    auth/
    users/
    categories/
    levels/
    challenges/
    evaluations/
    ai/
    trophies/
    leaderboard/
    analytics/
    common/
    config/
```

Each module owns:

* router.py
* service.py
* repository.py
* models.py
* schemas.py

---

# Frontend

```
frontend/

app/
components/
hooks/
services/
types/
lib/
styles/
```

---

# Documentation

```
docs/

product/
architecture/
development/
adr/
stories/
sprints/
templates/
```

---

# Ownership Rules

Every module owns:

* Business logic
* Validation
* Persistence

Modules communicate through services.

Repositories must never be called directly from another module.

---

# File: docs/development/GitWorkflow.md

# Git Workflow

Version: 1.0

---

# Branches

```
main

↓

develop

↓

feature/*
```

Examples

```
feature/authentication

feature/categories

feature/trophies
```

---

# Commit Format

Use Conventional Commits.

Examples

```
feat:

fix:

docs:

refactor:

test:

build:

chore:
```

Example

```
feat(auth): implement login endpoint
```

---

# Pull Requests

Each Pull Request should:

* Solve one logical problem.
* Reference the related Story.
* Include testing notes.
* Update documentation if necessary.

---

# Before Merging

Verify

* Tests pass
* Lint passes
* Documentation updated
* No secrets committed

---

# File: docs/development/Testing.md

# Testing Strategy

Version: 1.0

---

# Testing Pyramid

```
Unit Tests

↓

Integration Tests

↓

End-to-End Tests
```

---

# Unit Tests

Test:

* Business logic
* Validation
* Domain rules

Avoid:

* Database
* Network
* External APIs

---

# Integration Tests

Verify:

* API endpoints
* Database interaction
* Authentication
* Authorization

---

# End-to-End

Verify complete user flows.

Examples

* Register
* Login
* Solve challenge
* Earn trophy

---

# Test Principles

Tests should be:

* Independent
* Repeatable
* Readable
* Fast

---

# File: docs/development/Setup.md

# Development Setup

Version: 1.0

---

# Required Software

* Git
* Docker Desktop
* Python 3.13
* Node.js 22 LTS
* pnpm
* uv
* Cursor

---

# Repository

Recommended location

```
C:\Projects\CipherForge
```

---

# Backend

```
cd backend

uv venv

.venv\Scripts\activate
```

---

# Frontend

```
cd frontend

pnpm install
```

---

# Containers

```
docker compose up
```

---

# Verification

Ensure:

* Backend starts
* Frontend starts
* Database reachable
* Redis reachable

---

# Development Principles

* Develop inside feature branches.
* Run tests before committing.
* Keep documentation current.
* Never commit secrets or local configuration.
