from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, update
from app import schemas
from app.database.models import Task
from .dependencies import DEPENDS_ON_DB_SESSION

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
def create_task(task: schemas.TaskCreate, db: DEPENDS_ON_DB_SESSION) -> schemas.Task:
    db_model = Task(**task.model_dump())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


@router.get("/")
def get_all_tasks(db: DEPENDS_ON_DB_SESSION) -> list[schemas.Task]:
    tasks = db.query(Task).all()
    return [schemas.Task(**task.__dict__) for task in tasks]


@router.get("/{task_id}")
def get_task_by_id(task_id: int, db: DEPENDS_ON_DB_SESSION) -> schemas.Task:
    task = db.query(Task).where(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id {task_id} not found."
        )
    return task


@router.put("/{task_id}")
def update_task(
    task_id: int, task: schemas.TaskUpdate, db: DEPENDS_ON_DB_SESSION
) -> schemas.Task:
    task = db.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(**task.model_dump())
        .returning(Task)
    ).first()
    if task is None:
        raise HTTPException(status_code=404)
    db.commit()
    # db.refresh(task)
    return task[0]


@router.delete("/{task_id}")
def delete_task_by_id(task_id: int, db: DEPENDS_ON_DB_SESSION):
    task = db.execute(delete(Task).where(Task.id == task_id).returning(Task)).first()
    if task is None:
        raise HTTPException(status_code=404)
    task_id = task[0].id
    db.commit()
    return {"task_id": task_id}
