# capture-flag

> A learning-first cybersecurity platform that combines hands-on challenges, AI-powered role-playing scenarios, and gamification to help users develop practical security skills.

---

## Vision

Cyber Academy is designed to make cybersecurity learning engaging, structured, and practical. Unlike traditional Capture The Flag (CTF) platforms that primarily focus on competition, Cyber Academy emphasizes progressive learning through guided challenges, achievements, and real-world scenarios.

The platform is built with an AI-assisted development workflow, where implementation is performed by coding agents (such as Cursor or Codex) using structured stories, architectural documentation, and acceptance criteria.

---

## Project Goals

* Progressive cybersecurity learning
* AI-powered interactive challenges
* Gamified learning experience
* Modular and maintainable architecture
* Mobile-first user experience
* Production-ready engineering practices
* AI-friendly repository structure

---

## Non-Goals (Version 1)

The following are intentionally excluded from the initial release:

* Multi-tenancy
* Complex Role-Based Access Control (RBAC)
* Built-in vulnerable Docker/VM hosting
* Competition-focused scoring
* Challenge versioning
* Enterprise organization management

---

# Technology Stack

## Backend

* Python 3.13
* FastAPI
* SQLAlchemy 2.x
* PostgreSQL
* Redis
* Pydantic v2

## Frontend

* Next.js
* TypeScript
* Tailwind CSS
* shadcn/ui

## Infrastructure

* Docker
* Docker Compose

---

# Repository Structure

```text
cyber-academy/

├── backend/
├── frontend/
├── docker/
├── docs/
├── scripts/
├── .cursor/
├── .github/
├── .env.example
└── README.md
```

---

# Documentation

Project documentation is organized under the `docs/` directory.

| Document           | Purpose                         |
| ------------------ | ------------------------------- |
| Product.md         | Product vision and requirements |
| Architecture.md    | System architecture             |
| Database.md        | Database design                 |
| API.md             | API specifications              |
| TechStack.md       | Technology choices              |
| CodingStandards.md | Coding conventions              |
| AI_RULES.md        | Rules for AI coding agents      |
| Roadmap.md         | Project roadmap                 |
| Security.md        | Security guidelines             |
| UI_UX.md           | UI and UX guidelines            |

Additional folders:

```text
docs/

adr/
phases/
sprints/
stories/
templates/
context/
```

---

# Development Workflow

The project follows a structured delivery model.

```text
Phase
    ↓
Sprint
    ↓
Story
    ↓
Implementation
    ↓
Review
    ↓
Commit
```

Every feature begins with a Story document containing:

* Objective
* Background
* Acceptance Criteria
* Definition of Done
* Expected file changes
* Manual testing steps

---

# AI-Assisted Development

This repository is optimized for AI coding assistants such as:

* Cursor
* OpenAI Codex
* Claude Code (optional)

AI agents should always read the following documentation before implementation:

* `docs/Architecture.md`
* `docs/AI_RULES.md`
* Current Sprint document
* Current Story document

AI agents must never invent requirements or modify architecture without explicit approval.

---

# Branching Strategy

```text
main
│
└── develop
      │
      ├── feature/authentication
      ├── feature/categories
      ├── feature/challenges
      └── feature/leaderboard
```

Direct commits to `main` are discouraged.

---

# Development Principles

* Keep modules loosely coupled.
* Business logic belongs in services.
* Repositories only handle persistence.
* Routers only handle HTTP concerns.
* Follow Clean Architecture principles.
* Prefer readability over cleverness.
* Every change should be traceable to a Story.

---

# Project Status

Current Phase:

**Phase 0 – Foundation**

Current Sprint:

**Sprint 1 – Project Bootstrap**

---

# Contributing

Before implementing any feature:

1. Read the relevant Story document.
2. Follow the architecture documentation.
3. Follow the coding standards.
4. Follow the AI development rules.
5. Ensure all acceptance criteria are satisfied.

---

# License

License information will be added before the first public release.

---

# Maintainers

Cyber Academy Development Team
