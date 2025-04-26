import pytest
from app.database.config import engine, Base
from main import app
from fastapi.testclient import TestClient

# Set in-memory SQLite for testing
# os.environ["DATABASE_URL"] = "sqlite:///:memory:"


# Create the testing database and tables
@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)
