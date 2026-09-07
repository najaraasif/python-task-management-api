from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, status
from .models import TaskCreate, TaskResponse, TaskUpdate, get_db, init_db

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = str(BASE_DIR / "tasks.db")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db(DATABASE_PATH)
    yield


app = FastAPI(
    title="Python Task Management API",
    description="A RESTful task management API built with FastAPI and SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {
        "name": "Python Task Management API",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate):
    with get_db(DATABASE_PATH) as db:
        cursor = db.execute(
            """
            INSERT INTO tasks (title, description, completed)
            VALUES (?, ?, ?)
            """,
            (task.title, task.description, task.completed),
        )
        db.commit()
        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
        return dict(row)


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(
    completed: bool | None = None,
    search: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=100, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
):
    query = "SELECT * FROM tasks"
    conditions = []
    parameters = []

    if completed is not None:
        conditions.append("completed = ?")
        parameters.append(completed)

    if search is not None:
        conditions.append("(title LIKE ? OR description LIKE ?)")
        search_pattern = f"%{search}%"
        parameters.extend([search_pattern, search_pattern])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    parameters.extend([limit, skip])

    with get_db(DATABASE_PATH) as db:
        rows = db.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    with get_db(DATABASE_PATH) as db:
        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return dict(row)


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate):
    updates = task.model_dump(exclude_unset=True)

    with get_db(DATABASE_PATH) as db:
        existing = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        if updates:
            fields = []
            values = []
            for field, value in updates.items():
                fields.append(f"{field} = ?")
                values.append(value)
            values.append(task_id)

            db.execute(
                f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?",
                values,
            )
            db.commit()

        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
        return dict(row)


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int):
    with get_db(DATABASE_PATH) as db:
        cursor = db.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )
        db.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return None
