from fastapi import FastAPI
from app.routers.v1 import tasks
from app.database.config import Base, engine

Base.metadata.create_all(bind=engine)  # Creates all tables on startup (for dev)

app = FastAPI(title="Smart Task Manager API")
app.include_router(tasks.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
