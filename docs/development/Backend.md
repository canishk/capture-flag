# Backend Architecture

Version: 1.0

Status: Living Document

Related Documents

- docs/architecture/Overview.md
- docs/product/Requirements.md
- docs/development/CodingStandards.md

---

# Purpose

This document defines the backend architecture of CipherForge.

It describes how backend code should be organized, how modules communicate, and the architectural rules that every developer must follow.

This document intentionally avoids feature-specific implementation details.

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.13 | Programming Language |
| FastAPI | Web Framework |
| SQLAlchemy 2.x | ORM |
| Alembic | Database Migrations |
| PostgreSQL | Primary Database |
| Redis | Cache & Background Tasks |
| Pydantic v2 | Validation |
| Uvicorn | ASGI Server |
| Pytest | Testing |

---

# Architectural Style

CipherForge follows a **Modular Monolith** architecture.

Each domain is isolated into its own module.

Example:

```
Authentication

Users

Categories

Levels

Challenges

Evaluations

AI

Progress

Leaderboard

Administration
```

Each module owns its own:

- API
- Business Logic
- Persistence
- Validation

---

# Layered Architecture

Every request flows through the following layers.

```
HTTP Request

↓

Router

↓

Service

↓

Repository

↓

Database

↓

Repository

↓

Service

↓

Router

↓

HTTP Response
```

Each layer has a single responsibility.

---

# Layer Responsibilities

## Router

Responsible for:

- HTTP endpoints
- Request parsing
- Authentication
- Authorization
- Response formatting

Must NOT contain:

- Business logic
- SQL queries
- Complex validation

---

## Service

Responsible for:

- Business rules
- Orchestration
- Transactions
- Domain validation

Services should be framework-independent whenever practical.

---

## Repository

Responsible for:

- Database access
- Queries
- Persistence

Repositories should never contain business decisions.

---

## Models

Represent database entities.

Models should contain:

- Relationships
- Constraints
- Simple helper properties

Models should NOT contain business logic.

---

## Schemas

Use Pydantic models.

Responsibilities:

- Request validation
- Response serialization
- API contracts

---

# Backend Folder Structure

```
backend/

app/

    api/

    auth/

    users/

    categories/

    levels/

    challenges/

    evaluations/

    ai/

    progress/

    trophies/

    leaderboard/

    analytics/

    administration/

    common/

    config/

    database/

    middleware/

    dependencies/

    exceptions/

    models/

    schemas/

tests/

migrations/
```

---

# Standard Module Structure

Every domain module follows the same layout.

Example

```
categories/

router.py

service.py

repository.py

models.py

schemas.py

validators.py

exceptions.py
```

Additional files may be introduced when complexity requires.

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

Database → Service
```

Dependencies should always point downward.

---

# Dependency Injection

Use FastAPI dependency injection.

Dependencies include:

- Database Session
- Current User
- Configuration
- Cache
- External Services

Avoid creating dependencies manually inside business logic.

---

# Configuration

Configuration is environment-driven.

Configuration should be centralized.

Never hardcode:

- URLs
- Ports
- Secrets
- API Keys

---

# Error Handling

Errors are divided into:

- Validation Errors
- Authentication Errors
- Authorization Errors
- Domain Errors
- Infrastructure Errors

Every error should produce a predictable API response.

Unexpected exceptions should be logged.

---

# Logging

Use structured logging.

Every request should include:

- Request ID
- User ID (if authenticated)
- Timestamp
- Execution Time
- Status Code

Never log:

- Passwords
- Secrets
- Tokens
- Personal sensitive information

---

# Validation

Validation occurs in multiple layers.

## API Validation

Performed using Pydantic.

Examples:

- Required fields
- Data types
- Length
- Formats

---

## Business Validation

Performed in services.

Examples:

- Duplicate usernames
- Progress rules
- Challenge availability

---

## Database Validation

Performed using:

- Constraints
- Foreign Keys
- Unique Indexes

---

# Transactions

Business operations should execute within transactions when multiple database updates must succeed or fail together.

Keep transactions as short as possible.

---

# Background Processing

Long-running operations should not block HTTP requests.

Examples:

- Sending email
- AI processing
- Analytics aggregation
- Report generation

These tasks should execute asynchronously.

---

# Caching

Redis is used only for:

- Frequently accessed data
- Session-related data
- Rate limiting
- Temporary state

Redis is never the system of record.

---

# Authentication

Authentication is centralized.

Responsibilities include:

- Login
- Logout
- Password Hashing
- Token Validation

Authorization logic should remain separate from authentication.

---

# Authorization

Version 1 supports two roles.

- Administrator
- Learner

Role checks should be centralized and reusable.

---

# API Responses

Responses should follow a consistent structure.

Success

```json
{
  "success": true,
  "data": {}
}
```

Failure

```json
{
  "success": false,
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

---

# Module Communication

Modules should communicate through services.

Example

```
Challenge Service

↓

Progress Service

↓

Trophy Service
```

Avoid accessing another module's repository directly.

---

# Shared Components

Common functionality belongs under the shared infrastructure.

Examples

- Logging
- Exceptions
- Pagination
- Authentication
- Utilities
- Constants

Avoid duplicating shared logic.

---

# Testing Strategy

Each module should include:

- Unit Tests
- Integration Tests

Business logic should be testable without HTTP.

Repositories should be testable independently.

---

# Performance Guidelines

Prefer:

- Pagination
- Lazy loading where appropriate
- Batch operations
- Database indexes

Avoid:

- N+1 queries
- Large payloads
- Unnecessary database calls

Optimize only after measuring.

---

# Extensibility

Future modules should integrate without modifying existing modules whenever possible.

Examples

Future additions:

- Docker Lab Engine
- VM Challenges
- Marketplace
- Plugin Framework
- Community Challenges

The architecture should encourage extension rather than modification.

---

# Guiding Principles

Every backend implementation should satisfy the following:

- Single Responsibility Principle
- Explicit dependencies
- Predictable behavior
- Testability
- Readability
- Maintainability
- Security by default

When in doubt, choose the simpler design that preserves architectural consistency.