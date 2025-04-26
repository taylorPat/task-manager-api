# pydantic models
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    completed: bool = False


class Task(BaseModel):
    # Allow creating Pydantic models from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    completed: bool
