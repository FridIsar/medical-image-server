import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth import get_password_hash

client = TestClient(app)

# Create a test database and fixture for the tests
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Add a test user to the database
    test_user = User(username="testuser", hashed_password=get_password_hash("testpass"))
    db.add(test_user)
    db.commit()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_login_success(test_db):
    response = client.post("/login", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure(test_db):
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
