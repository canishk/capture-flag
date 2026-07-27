# CipherForge Backend

FastAPI modular monolith for the CipherForge learning platform.

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
```

## Run

```bash
uvicorn app.main:app --reload
```

## Migrations

```bash
alembic upgrade head
```

## Tests

```bash
pytest
```
