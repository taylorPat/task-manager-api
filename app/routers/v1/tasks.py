from fastapi import APIRouter, HTTPException
from sqlalchemy import delete, update
from app import schemas
import app.database.models as db_models
from ..dependencies import DEPENDS_ON_DB_SESSION

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.post("/")
def create_task(task: schemas.TaskCreate, db: DEPENDS_ON_DB_SESSION) -> schemas.Task:
    db_model = db_models.Task(**task.model_dump())
    db.add(db_model)  # record queued inside the session, ready to be saved
    db.commit()  # saves / inserts everything in the queue to the db
    db.refresh(db_model)  # gets the object again from the db with the latest fields
    return db_model


@router.get("/")
def get_all_tasks(db: DEPENDS_ON_DB_SESSION) -> list[schemas.Task]:
    tasks = db.query(db_models.Task).all()
    return [schemas.Task.model_validate(task) for task in tasks]


@router.get("/{task_id}")
def get_task_by_id(task_id: str, db: DEPENDS_ON_DB_SESSION) -> schemas.Task:
    task = db.query(db_models.Task).where(db_models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=404, detail=f"Task with id {task_id} not found."
        )
    return task


@router.put("/{task_id}")
def update_task_by_id(
    task_id: str, task: schemas.TaskUpdate, db: DEPENDS_ON_DB_SESSION
) -> schemas.Task:
    task = db.execute(
        update(db_models.Task)
        .where(db_models.Task.id == task_id)
        .values(**task.model_dump())
        .returning(db_models.Task)
    ).first()
    if task is None:
        raise HTTPException(status_code=404)
    db.commit()
    return task[0]


@router.delete("/{task_id}")
def delete_task_by_id(task_id: str, db: DEPENDS_ON_DB_SESSION):
    task = db.execute(
        delete(db_models.Task)
        .where(db_models.Task.id == task_id)
        .returning(db_models.Task)
    ).first()
    if task is None:
        raise HTTPException(status_code=404)
    task_id = task[0].id
    db.commit()
    return {"task_id": task_id}
