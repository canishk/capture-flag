# Naming Conventions

Version: 1.0

Status: Living Document

Related Documents

- docs/architecture/Overview.md
- docs/architecture/Backend.md
- docs/architecture/ModuleStandards.md
- docs/development/CodingStandards.md

---

# Purpose

This document defines the naming conventions used throughout the CipherForge project.

Consistent naming improves readability, maintainability, and discoverability. All contributors should follow these conventions unless an approved Architectural Decision Record (ADR) specifies otherwise.

---

# General Principles

- Prefer descriptive names over abbreviations.
- Use complete words where practical.
- Avoid project-specific acronyms unless they are well known.
- Be consistent rather than clever.
- Names should describe intent, not implementation.

Examples:

Good

```
challenge_score
user_progress
is_completed
```

Avoid

```
cs
usrProg
flag1
tmp
obj
```

---

# File Naming

## Python

Use **snake_case**.

Examples

```
challenge_service.py
progress_repository.py
leaderboard_router.py
```

---

## React / TypeScript

Components use **PascalCase**.

```
ChallengeCard.tsx
LoginForm.tsx
AdminDashboard.tsx
```

Other TypeScript files use **camelCase** or **kebab-case** according to project tooling.

```
apiClient.ts
dateUtils.ts
```

---

# Folder Naming

Use lowercase **snake_case** for backend modules.

```
users
categories
progress
leaderboard
```

Frontend folders should remain lowercase.

```
components
hooks
services
styles
```

---

# Class Naming

Use **PascalCase**.

Examples

```
User
Challenge
ProgressService
UserRepository
ChallengeResponse
```

Never use underscores in class names.

---

# Function Naming

Use **snake_case** in Python.

```
create_user()
unlock_level()
calculate_score()
```

Use **camelCase** in TypeScript.

```
createUser()
unlockLevel()
calculateScore()
```

Function names should begin with a verb.

---

# Variable Naming

Use meaningful names.

```
current_user
completed_levels
challenge_points
```

Avoid

```
x
value
data
temp
```

Boolean variables should read naturally.

```
is_active
is_completed
has_permission
can_edit
```

---

# Constants

Python constants use **UPPER_SNAKE_CASE**.

```
MAX_LOGIN_ATTEMPTS
DEFAULT_PAGE_SIZE
JWT_EXPIRATION_MINUTES
```

Module-specific constants belong in `constants.py`.

---

# Environment Variables

Use **UPPER_SNAKE_CASE**.

```
DATABASE_URL
REDIS_URL
JWT_SECRET_KEY
OPENAI_API_KEY
LOG_LEVEL
```

Prefix related settings when appropriate.

```
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DATABASE
```

---

# Database Naming

## Tables

Use **snake_case**.

Prefer singular table names.

```
user
challenge
category
progress
trophy
```

---

## Primary Keys

Use a consistent name:

```
id
```

Type is defined in the database design document (UUID or integer).

---

## Foreign Keys

Use:

```
user_id
challenge_id
category_id
```

Never abbreviate.

---

## Columns

Use **snake_case**.

Examples

```
created_at
updated_at
completed_at
display_name
attempt_count
```

Avoid

```
CreateDate
dt
usrName
```

---

## Boolean Columns

Prefix with:

```
is_
has_
can_
```

Examples

```
is_active
is_deleted
has_completed
can_retry
```

---

## Timestamp Columns

Every persistent entity should include, where applicable:

```
created_at
updated_at
deleted_at
```

Store timestamps in UTC.

---

# API Naming

## Resource Names

Use plural nouns.

```
/users
/challenges
/categories
/levels
/trophies
```

Avoid verbs in resource names.

Good

```
POST /users
DELETE /users/{id}
```

Avoid

```
/createUser
/deleteChallenge
```

---

## Query Parameters

Use **snake_case**.

```
page
page_size
sort_by
search
is_active
```

---

# JSON Naming

Use **camelCase** for JSON payloads.

Example

```json
{
  "displayName": "Alice",
  "challengePoints": 120,
  "isCompleted": true
}
```

The backend may internally use `snake_case`, but API contracts should expose a consistent JSON style.

---

# Pydantic Schemas

Request models

```
UserCreateRequest
UserUpdateRequest
LoginRequest
```

Response models

```
UserResponse
ChallengeResponse
ProgressResponse
```

Shared models

```
PaginationResponse
ApiError
```

---

# SQLAlchemy Models

Use singular **PascalCase**.

```
User
Challenge
Category
Progress
```

Model names should match business entities.

---

# Service Classes

Suffix with `Service`.

```
UserService
ChallengeService
ProgressService
```

---

# Repository Classes

Suffix with `Repository`.

```
UserRepository
CategoryRepository
```

---

# Validators

Name according to responsibility.

```
ProgressValidator
ChallengeValidator
```

Methods should begin with verbs.

```
validate_submission()
validate_unlock()
```

---

# Exceptions

End exception names with `Error`.

```
ChallengeNotFoundError
DuplicateCategoryError
InvalidProgressError
AuthenticationError
```

Exception names should clearly describe the problem.

---

# Events

Use past tense.

```
UserRegistered
ChallengeCompleted
TrophyUnlocked
LevelUnlocked
```

---

# React Components

Use PascalCase.

```
ChallengeCard
ProgressBar
LeaderboardTable
```

---

# React Hooks

Prefix with `use`.

```
useAuth
useChallenges
useLeaderboard
```

---

# CSS Classes

Prefer Tailwind utility classes.

When custom classes are required, use lowercase kebab-case.

```
challenge-card
admin-layout
```

---

# Docker

Container names

```
backend
frontend
postgres
redis
```

Networks

```
cipherforge-network
```

Volumes

```
postgres-data
redis-data
```

---

# Git Branches

Use lowercase.

```
feature/authentication
feature/challenge-engine
bugfix/login-timeout
docs/backend-architecture
refactor/progress-service
```

---

# Commit Messages

Follow Conventional Commits.

```
feat(auth): add JWT authentication
fix(progress): resolve duplicate unlock issue
docs(api): update pagination guidelines
refactor(repository): simplify challenge queries
```

---

# Test Naming

Test files

```
test_user_service.py
test_progress_repository.py
```

Test functions

```
test_create_user_success()
test_unlock_level_requires_previous_level()
test_duplicate_category_returns_conflict()
```

Test names should describe expected behavior.

---

# Abbreviations

Avoid abbreviations unless they are industry standard.

Acceptable

```
API
JWT
URL
UUID
HTTP
JSON
SQL
CSV
AI
```

Avoid

```
cfg
usr
cat
lvl
prog
```

---

# Reserved Names

Do not use generic names such as:

```
utils
helper
misc
common_functions
manager
processor
```

Choose names that describe the actual responsibility.

---

# Consistency Rule

When multiple valid names exist, always prefer the one already established in the project.

Consistency across the codebase is more valuable than individual preference.

---

# Summary

The naming conventions can be summarized as follows:

| Element | Convention |
|----------|------------|
| Python files | snake_case |
| Python functions | snake_case |
| Python variables | snake_case |
| Python classes | PascalCase |
| Database tables | snake_case (singular) |
| Database columns | snake_case |
| Primary key | id |
| Foreign keys | `<entity>_id` |
| API routes | plural nouns |
| JSON properties | camelCase |
| React components | PascalCase |
| React hooks | useCamelCase |
| Environment variables | UPPER_SNAKE_CASE |
| Constants | UPPER_SNAKE_CASE |
| Git branches | lowercase with prefixes |
| Commit messages | Conventional Commits |