# 📝 Task Manager API

Simple, clean FastAPI + SQLAlchemy 2.0 project for managing tasks.

## 🚀 Features

- Create, read, update, and delete tasks
- Modern FastAPI app
- SQLAlchemy 2.0 with full typing
- Pydantic v2 schemas
- SQLite
- uv for dependency management

## 🛠 Installation

```bash
git clone https://github.com/taylorPat/task-manager-api.git
cd task-manager-api
uv sync --all-groups # installs also the linting dependency group
```

## 🧪 Local development

Creat _.env_ file:

```env
DATABASE_URL = "sqlite:///./task.db"
```

```bash
# run tests
uv run pytest
# format
uv run ruff format .
# lint
uv run ruff check .
```

## 🏃 Running the app

```bash
uv run main.py
```

> [!NOTE]  
> Swagger UI: http://127.0.0.1:8000/docs
