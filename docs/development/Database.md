
# Database Architecture

Version: 1.0

Status: Living Document

Related Documents

- docs/architecture/Overview.md
- docs/architecture/Backend.md
- docs/architecture/ModuleStandards.md
- docs/architecture/NamingConventions.md
- docs/product/Requirements.md

---

# Purpose

This document defines the database architecture, design principles, and data management standards for CipherForge.

It establishes how data is modeled, stored, related, indexed, and evolved over time.

This document intentionally focuses on architectural principles rather than feature-specific schemas.

---

# Database Technology

| Component | Technology |
|------------|------------|
| Primary Database | PostgreSQL |
| ORM | SQLAlchemy 2.x |
| Migration Tool | Alembic |
| Cache | Redis |

PostgreSQL is the system of record.

Redis must never contain authoritative business data.

---

# Database Design Principles

The database should prioritize:

- Data integrity
- Simplicity
- Consistency
- Maintainability
- Predictable performance
- Future extensibility

The database should model the business domain rather than application implementation details.

---

# Data Ownership

Each business module owns its data.

Example:

```
Users
    owns user data

Challenges
    owns challenge data

Progress
    owns progress data

Leaderboard
    owns leaderboard data
```

Other modules access data through services rather than directly modifying another module's tables.

---

# Entity Design

Each entity should represent one business concept.

Good examples:

- User
- Challenge
- Category
- Level
- Trophy

Avoid tables that mix unrelated concerns.

---

# Primary Keys

All major entities use:

```
id UUID
```

Requirements:

- Globally unique
- Immutable
- Never reused
- Never reassigned

Primary keys should have no business meaning.

---

# Foreign Keys

Foreign keys use the naming convention:

```
user_id
challenge_id
category_id
```

All relationships should use explicit foreign key constraints.

---

# Relationship Principles

Prefer explicit relationships.

Supported relationship types:

- One-to-One
- One-to-Many
- Many-to-Many (via junction tables)

Avoid storing comma-separated IDs or serialized relationships.

---

# Normalization

Target Third Normal Form (3NF) for transactional data.

Normalization goals:

- Reduce duplication
- Improve consistency
- Simplify updates

Denormalization should only be introduced after measuring performance benefits.

---

# Audit Fields

Every persistent entity should include:

```
id
created_at
updated_at
```

Entities supporting soft deletion additionally include:

```
deleted_at
```

All timestamps are stored in UTC.

---

# Soft Deletes

Use soft deletes only where business recovery is required.

Example:

- Users
- Challenges
- Categories

Avoid soft deletes for:

- Audit logs
- Junction tables
- Ephemeral data

---

# Naming Standards

Follow `docs/architecture/NamingConventions.md`.

Summary:

- snake_case
- singular table names
- descriptive column names

Examples:

```
user

challenge

challenge_submission
```

---

# Data Types

Prefer explicit types.

Examples:

| Purpose | Type |
|----------|------|
| Identifier | UUID |
| Name | VARCHAR |
| Description | TEXT |
| Boolean | BOOLEAN |
| Timestamp | TIMESTAMP WITH TIME ZONE |
| Counter | INTEGER |
| Score | INTEGER |
| Metadata | JSONB (when appropriate) |

Avoid generic text fields for structured data.

---

# JSON Usage

JSONB should be used only when:

- Structure is flexible
- Data is not frequently queried
- Schema changes rapidly

Business-critical fields should remain relational.

---

# Constraints

Use database constraints whenever possible.

Examples:

- NOT NULL
- UNIQUE
- FOREIGN KEY
- CHECK

Business validation remains the responsibility of the service layer.

---

# Indexing Strategy

Create indexes for:

- Foreign keys
- Frequently filtered columns
- Frequently sorted columns
- Frequently searched columns

Examples:

```
created_at

email

username

category_id
```

Avoid unnecessary indexes that increase write costs.

---

# Transactions

Transactions should be:

- Short
- Atomic
- Consistent

Business workflows spanning multiple tables should execute within a single transaction.

---

# Concurrency

Design for optimistic concurrency where practical.

Avoid long-running transactions.

Use row locking only when necessary.

---

# Cascading Rules

Prefer explicit application behavior over cascading deletes.

Recommended:

```
ON DELETE RESTRICT
```

or

```
ON DELETE SET NULL
```

Use cascading deletes only when ownership is absolute.

---

# Migrations

All schema changes must be performed through Alembic migrations.

Never modify production schemas manually.

Migration rules:

- One logical change per migration
- Reversible where practical
- Small and reviewable

---

# Schema Evolution

Database changes should be backward compatible whenever possible.

Recommended sequence:

1. Add new column.
2. Deploy application.
3. Backfill data.
4. Remove deprecated column in a later release.

Avoid breaking changes in a single deployment.

---

# Data Integrity

Integrity should be enforced at multiple layers:

1. API validation
2. Business validation
3. Database constraints

The database is the final authority for structural integrity.

---

# Performance Guidelines

Prefer:

- Indexed lookups
- Pagination
- Batch operations
- Efficient joins

Avoid:

- SELECT *
- N+1 query patterns
- Excessive nested queries
- Large unbounded result sets

Measure before optimizing.

---

# Archival Strategy

Historical data should be retained where required.

Potential archival candidates:

- Audit logs
- User activity
- Challenge attempts

Archival policies should be defined per module.

---

# Backup Strategy

Production databases must support:

- Daily backups
- Point-in-time recovery
- Restore verification
- Disaster recovery procedures

Backups should be encrypted.

---

# Security

Sensitive information should never be stored in plain text.

Examples:

- Passwords → hashed
- Secrets → encrypted
- Tokens → hashed or encrypted as appropriate

Database access should follow the principle of least privilege.

---

# Multi-Tenancy

Version 1 does **not** support multi-tenancy.

Do not introduce tenant identifiers or tenant-aware schemas unless a future ADR approves this architectural change.

---

# Module Boundaries

Tables should remain aligned with module ownership.

Example:

```
Users
    user

Challenges
    challenge

Progress
    progress

Leaderboard
    leaderboard_entry
```

Cross-module joins should be minimized and justified by use cases.

---

# Read vs. Write Models

Version 1 uses a single relational model for both reads and writes.

CQRS is intentionally out of scope.

---

# Future Evolution

The architecture should support future additions such as:

- Analytics warehouse
- Read replicas
- Search indexing
- Event streaming
- Distributed services

These should integrate without requiring fundamental changes to the transactional schema.

---

# Database Review Checklist

Before introducing a new table, confirm:

- Does it represent a single business concept?
- Does another module already own this data?
- Are relationships explicit?
- Are constraints defined?
- Are indexes justified?
- Are audit fields included?
- Is the naming consistent?
- Is the migration reversible?
- Is the design documented?

---

# Guiding Principle

The database is a long-lived asset.

Application code changes frequently.

Database schemas should evolve deliberately, conservatively, and with backward compatibility whenever practical.