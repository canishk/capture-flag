# CipherForge

Learning-first cybersecurity platform.

## Quick start

```bash
cp .env.example .env
docker compose -f docker/docker-compose.yml up -d postgres redis
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

## Sprint 1 scope

- Authentication (register, login, logout, refresh, password reset/change, email verify)
- Users (profile, avatar, admin list/disable/enable)
- PostgreSQL migrations
- Event dispatcher + audit logging

## Tests

```bash
cd backend
pytest
```
