from typing import Annotated

from fastapi import Depends
from app.database.config import SessionLocal
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DEPENDS_ON_DB_SESSION = Annotated[Session, Depends(get_db)]
