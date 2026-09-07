import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "test_tasks.db"
    init_db(str(db_path))

    monkeypatch.setattr("app.main.DATABASE_PATH", str(db_path))

    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn FastAPI",
            "description": "Build a REST API",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI"
    assert data["description"] == "Build a REST API"
    assert data["completed"] is False
    assert "created_at" in data


def test_create_task_with_invalid_title(client):
    response = client.post(
        "/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422


def test_create_task_with_long_title(client):
    response = client.post(
        "/tasks",
        json={"title": "A" * 101},
    )

    assert response.status_code == 422


def test_get_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Test task"},
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Test task"


def test_get_nonexistent_task(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_completed_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Completed task", "completed": True},
    )
    client.post(
        "/tasks",
        json={"title": "Pending task", "completed": False},
    )

    response = client.get("/tasks?completed=true")

    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Completed task"


def test_search_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Learn FastAPI"},
    )
    client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )

    response = client.get("/tasks?search=FastAPI")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Learn FastAPI"


def test_pagination(client):
    for number in range(1, 4):
        client.post(
            "/tasks",
            json={"title": f"Task {number}"},
        )

    response = client.get("/tasks?limit=1&skip=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Task 2"


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"},
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated title",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is True


def test_partial_update(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "Original description",
        },
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Original title"
    assert data["description"] == "Original description"
    assert data["completed"] is True


def test_update_nonexistent_task(client):
    response = client.put(
        "/tasks/999",
        json={"title": "Updated"},
    )

    assert response.status_code == 404


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Delete me"},
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404


def test_delete_nonexistent_task(client):
    response = client.delete("/tasks/999")

    assert response.status_code == 404


def test_database_schema(tmp_path):
    db_path = tmp_path / "schema_test.db"

    init_db(str(db_path))

    connection = sqlite3.connect(db_path)

    columns = connection.execute(
        "PRAGMA table_info(tasks)"
    ).fetchall()

    connection.close()

    column_names = [column[1] for column in columns]

    assert column_names == [
        "id",
        "title",
        "description",
        "completed",
        "created_at",
    ]
