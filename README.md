# Python Task Management API

A production-style RESTful Task Management API built with Python, FastAPI, Pydantic, and SQLite.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-green)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/Tests-16%20Passing-brightgreen)](#testing)
[![CI](https://github.com/najaraasif/python-task-management-api/actions/workflows/tests.yml/badge.svg)](https://github.com/najaraasif/python-task-management-api/actions/workflows/tests.yml)

## Overview

This project implements a lightweight REST API for managing tasks. It demonstrates practical backend development concepts including RESTful API design, request validation, SQLite persistence, CRUD operations, filtering, search, pagination, HTTP status codes, and automated testing.

## Features

- Create, retrieve, update, and delete tasks
- Pydantic request and response validation
- SQLite database persistence
- Completed-status filtering
- Task search by title or description
- Pagination with limit and offset
- Proper HTTP status codes
- 404 handling for missing tasks
- Automatic interactive Swagger documentation
- Isolated SQLite database testing
- 16 automated pytest tests
- Database schema verification

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API framework |
| Pydantic | Data validation and serialization |
| SQLite | Persistent data storage |
| pytest | Automated testing |
| HTTPX | API test client support |
| Uvicorn | ASGI application server |

## Project Structure

```text
python-task-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/najaraasif/python-task-management-api.git
cd python-task-management-api
```

### 2. Create a virtual environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

## API Documentation

FastAPI automatically provides interactive API documentation.

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **OpenAPI specification**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

## API Reference

| Method | Endpoint | Description | Success |
|---|---|---|---|
| GET | `/` | Health check | 200 |
| POST | `/tasks` | Create a task | 201 |
| GET | `/tasks` | List tasks | 200 |
| GET | `/tasks/{task_id}` | Get a task | 200 |
| PUT | `/tasks/{task_id}` | Update a task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

- **Missing tasks return**: `404 Not Found`
- **Invalid request data returns**: `422 Unprocessable Entity`

## Example Requests

### Create a task
```bash
curl -X POST "http://127.0.0.1:8000/tasks" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn FastAPI\",\"description\":\"Build a REST API\"}"
```

**Example response:**
```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build a REST API",
  "completed": false,
  "created_at": "2026-09-07T09:00:00"
}
```

### List tasks
```bash
curl "http://127.0.0.1:8000/tasks"
```

### Filter completed tasks
```bash
curl "http://127.0.0.1:8000/tasks?completed=true"
```

### Search tasks
```bash
curl "http://127.0.0.1:8000/tasks?search=FastAPI"
```

### Pagination
```bash
curl "http://127.0.0.1:8000/tasks?limit=10&skip=0"
```

### Get a task
```bash
curl "http://127.0.0.1:8000/tasks/1"
```

### Update a task
```bash
curl -X PUT "http://127.0.0.1:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d "{\"completed\":true}"
```

### Delete a task
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

## Testing

The project uses pytest with an isolated SQLite database for deterministic API tests.

**Run tests:**
```bash
pytest -v
```

**Current test coverage includes:**
- Health endpoint
- Task creation
- Input validation
- Maximum title length validation
- Task retrieval
- Missing task handling
- Task listing
- Completed-task filtering
- Search
- Pagination
- Full updates
- Partial updates
- Missing-task updates
- Task deletion
- Missing-task deletion
- SQLite schema validation

**Current result:**
```text
16 passed
```

## Design Notes

- The API separates request validation from database operations.
- Pydantic models define the expected API data structures, while SQLite handles persistence.
- Tests use temporary databases so test execution does not modify the application's production database.
- Parameterized SQL queries are used for database operations to avoid directly interpolating user-provided values into SQL statements.

## Future Improvements

Potential extensions include:
- User authentication and authorization
- Task ownership
- Sorting options
- Due dates
- Priority levels
- Database migrations
- PostgreSQL support
- Docker support
- CI/CD with GitHub Actions
- API rate limiting

## Author

**Aasif**  
Web and App Developer focused on Python, APIs, testing, and practical software development.  
GitHub: [https://github.com/najaraasif](https://github.com/najaraasif)