# t-board-backend

Hi, this is the small backend that powers the "t-board". It's intentionally tiny and focused: a Django + Django REST Framework API that stores tasks and exposes a simple CRUD interface for a frontend to consume.

how the project is organized, how to run it, how the API is protected, and a few notes for production.

## A quick mental model

- It's Django 6 with DRF. Very little ceremony.
- One app: `tasks` (models, serializers, views, URLs). The `core` module holds global settings and a tiny middleware.
- Uses SQLite by default for convenience (see `core/settings.py`). Swap to Postgres in production.
- All API routes under `/api/` are protected by a simple API key provided via `X-API-KEY`.

## What matters in the code

- `core/settings.py` — environment-driven settings. Loads `.env` in development.
- `core/middleware.py` — checks `X-API-KEY` for requests under `/api/` and returns 401/500 if missing or misconfigured.
- `tasks/models.py` — `Task` model: title, description, status, priority, due date, created_at.
- `tasks/serializers.py` — serializer-level validation (title not blank, choice validation).
- `tasks/views.py` + `tasks/urls.py` — endpoints (list/create and retrieve/update/delete).

## The Task model

Fields you care about:
- `title` (required, non-blank)
- `description` (optional)
- `status` — one of BACKLOG, IN_PROGRESS, DONE
- `priority` — one of LOW, MEDIUM, HIGH
- `due_date` — optional ISO date
- `created_at` — auto timestamp

Validation happens in two places: the serializer (good error messages for clients) and the database (CHECK constraints to avoid invalid writes). That gives you friendly API errors and a safety net at persistence level.

## How the API is secured

This project uses a very small, explicit pattern: an API key that the server reads from the `API_KEY` environment variable. Requests to routes beginning with `/api/` must include that key in the `X-API-KEY` header. If the server has no `API_KEY` configured it returns 500 (we prefer to fail-fast), and if a request is missing or has the wrong key it returns 401.

Example quick request:

```bash
curl -H "X-API-KEY: $API_KEY" http://localhost:8000/api/tasks/
```

This is intentionally minimal — perfect for demos, prototypes, or internal tools. If you need per-user auth, scopes, or delegated access, consider swapping this for a proper auth system (JWT, OAuth2, or Django sessions depending on your needs).

## Important environment variables

- `SECRET_KEY` — Django secret. Must be set when `DEBUG=false`.
- `DEBUG` — `true` / `false` (defaults to `true` locally).
- `ALLOWED_HOSTS` — comma-separated list for production.
- `CORS_ALLOWED_ORIGINS` — comma-separated origins (e.g. `http://localhost:3000`).
- `API_KEY` — the key the middleware checks for requests under `/api/`.
- `ANON_RATE` — DRF throttle for anonymous requests (default `100/day`).

A short `.env` example (never commit this):

```
SECRET_KEY=dev-secret-key
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
API_KEY=please-change-me
ANON_RATE=100/day
```

## Run it locally 

1. Create and activate a venv

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Create a `.env` like the snippet above 

4. Migrate the database

```bash
python manage.py migrate
```

5. (Optional) create a superuser

```bash
python manage.py createsuperuser
```

6. Start the server

```bash
python manage.py runserver
```

Open `http://localhost:8000/api/tasks/` with the `X-API-KEY` header and you’ll see the list endpoint.

## Endpoints

- GET  /api/tasks/        — list tasks (newest first)
- POST /api/tasks/        — create a task
- GET  /api/tasks/<id>/   — read one
- PUT/PATCH /api/tasks/<id>/ — update
- DELETE /api/tasks/<id>/ — delete

Body for create/update (JSON):

```json
{
  "title": "Write README",
  "description": "Make it friendly and useful",
  "status": "BACKLOG",
  "priority": "MEDIUM",
  "due_date": "2025-08-31"
}
```

Responses include `id` and `created_at` (read-only). The API returns clear validation messages for bad input.

## Tests

Run the existing test suite with Django’s runner:

```bash
python manage.py test
```


