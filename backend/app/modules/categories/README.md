# Categories Module

## Purpose

Organizes CipherForge learning content into subject areas (Web Security, Cryptography, etc.).

## Responsibilities

- Category CRUD (admin)
- Display ordering
- Visibility (active / hidden)
- Domain events for downstream consumers

## Public API

- `GET /api/v1/categories`
- `GET /api/v1/categories/{categoryId}`
- `POST /api/v1/categories` (admin)
- `PATCH /api/v1/categories/{categoryId}` (admin)
- `DELETE /api/v1/categories/{categoryId}` (admin hide)
- `POST /api/v1/categories/{categoryId}/restore` (admin)
- `PATCH /api/v1/categories/{categoryId}/order` (admin)

## Dependencies

- Shared infrastructure only (audit, events, database)
- No direct dependency on Levels, Challenges, or Progress

## Events Published

- `CategoryCreated`
- `CategoryUpdated`
- `CategoryHidden`

## Service Interface

Other modules should use `CategoryService.category_exists()` or public read APIs — never `CategoryRepository` directly.
