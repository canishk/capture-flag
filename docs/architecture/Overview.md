# CipherForge Architecture Overview

Version: 1.0

Status: Living Document

Related Documents

- docs/product/Vision.md
- docs/product/Requirements.md

---

# Purpose

This document describes the high-level architecture of CipherForge.

Its purpose is to establish architectural boundaries, define system responsibilities, and document how the major components interact.

Implementation details such as API endpoints, database schema, and deployment configuration are intentionally documented elsewhere.

---

# Architectural Principles

CipherForge follows these core principles:

- Modular Monolith
- Domain Driven Design (lightweight)
- Layered Architecture
- API First
- Mobile First
- Security by Design
- AI Assisted Development
- Cloud Ready

---

# Why Modular Monolith?

Version 1 is intentionally designed as a Modular Monolith.

Reasons:

- Simpler deployment
- Faster development
- Easier debugging
- Lower operational complexity
- Easier testing
- Clear module boundaries

Modules are designed so they can become independent services in the future if required.

---

# System Overview

```
                        Browser
                           │
                    Next.js Frontend
                           │
                     REST API (HTTPS)
                           │
                     FastAPI Backend
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    Service Layer     Infrastructure     Shared Components
         │
    Repository Layer
         │
      PostgreSQL
         │
       Redis Cache
```

---

# High Level Components

The system consists of the following major components.

## Frontend

Responsibilities:

- User Interface
- Routing
- State Management
- Authentication UI
- Responsive Design

The frontend should contain no business logic beyond presentation concerns.

---

## Backend

Responsibilities:

- Business Logic
- Authentication
- Authorization
- Validation
- Progress Tracking
- Challenge Evaluation
- Trophy Engine
- Analytics

---

## Database

Responsibilities:

- Persistent Storage
- Referential Integrity
- Transaction Management

The database should never contain application business logic.

---

## Cache

Redis is used for:

- Session data
- Frequently accessed data
- Rate limiting
- Temporary values

Redis is not the primary source of truth.

---

## AI Providers

AI functionality is accessed through an abstraction layer.

Supported providers may include:

- OpenAI
- Groq
- Ollama (future)

The application should not depend directly on a single provider.

---

# Architectural Layers

CipherForge follows a strict layered architecture.

```
Presentation

↓

Application

↓

Domain

↓

Infrastructure

↓

Database
```

---

## Presentation Layer

Responsibilities:

- HTTP Endpoints
- Request Validation
- Authentication
- Response Formatting

Should never contain business rules.

---

## Application Layer

Responsibilities:

- Use Cases
- Business Logic
- Orchestration
- Transactions

This is where most application logic lives.

---

## Domain Layer

Responsibilities:

- Business Rules
- Domain Models
- Domain Services
- Domain Events (future)

The domain layer should remain independent from frameworks.

---

## Infrastructure Layer

Responsibilities:

- Database Access
- External APIs
- AI Providers
- Storage
- Email
- Logging

Infrastructure implements interfaces defined by higher layers.

---

# Dependency Rules

Dependencies always point downward.

```
Router

↓

Service

↓

Repository

↓

Database
```

Forbidden dependencies:

- Router → Database
- Router → SQLAlchemy Models
- Repository → Router
- Database → Services

---

# Module Structure

Each module owns its own functionality.

Example:

```
categories/

router.py

service.py

repository.py

models.py

schemas.py

validators.py
```

Modules communicate through service interfaces rather than accessing each other's repositories directly.

---

# Planned Modules

Version 1 contains the following domains.

Authentication

Users

Categories

Levels

Challenges

Evaluations

AI

Progress

Trophies

Leaderboard

Analytics

Administration

Common

Configuration

---

# Cross Cutting Concerns

Shared capabilities include:

- Authentication
- Logging
- Configuration
- Exception Handling
- Validation
- Rate Limiting
- Monitoring

These concerns should be implemented centrally.

---

# API Design

The backend exposes REST APIs.

General principles:

- Versioned endpoints
- Stateless communication
- JSON payloads
- Consistent error responses
- Standard HTTP status codes

---

# Error Handling

Errors should be:

- Predictable
- Structured
- Logged
- User friendly

Internal implementation details should never be exposed to clients.

---

# Security Principles

The architecture follows secure-by-default principles.

Examples:

- Input validation
- Parameterized queries
- Password hashing
- JWT authentication
- HTTPS in production
- Principle of Least Privilege

---

# Scalability

The architecture should support future growth without major redesign.

Examples include:

- Additional AI providers
- New challenge types
- Additional evaluation engines
- Enterprise features
- Microservice extraction

Each module should be independently evolvable.

---

# Extensibility

Future features should be introduced by adding modules rather than modifying existing ones whenever possible.

Examples:

- Docker Lab Engine
- VM Engine
- Marketplace
- Community Challenges
- Plugin Framework

---

# Architectural Constraints

Version 1 intentionally avoids:

- Distributed microservices
- Event-driven architecture
- CQRS
- Event sourcing
- Multiple databases
- Multi-tenancy

These decisions reduce operational complexity while keeping the architecture flexible.

---

# Quality Attributes

The architecture prioritizes:

1. Maintainability
2. Simplicity
3. Readability
4. Security
5. Testability
6. Performance
7. Extensibility

Performance optimizations should never significantly reduce maintainability without measurable benefit.

---

# Architectural Decision Records

Major architectural decisions are documented separately under:

```
docs/adr/
```

The Architecture Overview should describe the current architecture, while ADRs explain why specific decisions were made.

---

# Guiding Principle

The architecture should make it easy to add new features while minimizing the impact on existing functionality.

A developer should be able to modify one module without needing to understand the entire system.