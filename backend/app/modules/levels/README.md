# Levels Module

## Purpose

Learning progression stages within a category.

## Responsibilities

- Level CRUD, ordering, visibility, unlock configuration storage

## Public API

- `GET /api/v1/levels`
- `GET /api/v1/levels/{levelId}`
- `POST /api/v1/levels` (admin)
- `PATCH /api/v1/levels/{levelId}` (admin)
- `DELETE /api/v1/levels/{levelId}` (admin hide)
- `POST /api/v1/levels/{levelId}/restore` (admin)
- `PATCH /api/v1/levels/{levelId}/order` (admin)

## Dependencies

- `CategoryService` for category validation (not `CategoryRepository`)

## Events

- `LevelCreated`, `LevelUpdated`, `LevelHidden`
