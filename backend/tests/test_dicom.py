import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import User
from app.auth import get_password_hash
from app.auth import create_access_token

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

# Dummy JWT token generation for authorization
@pytest.fixture(scope="module")
def token():
    # Generate a valid token for the test user
    return create_access_token(data={"sub": "testuser"})

def test_retrieve_patient_name_success(token, test_db):
    response = client.get(
        "/patient-name?dicom_filename=test/example.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "patient_name" in response.json()
    assert response.json()["patient_name"] == "PatientName"

def test_missing_dicom_file(token, test_db):
    response = client.get(
        "/patient-name?dicom_filename=missing.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "DICOM file not found"

def test_invalid_dicom_file(token, test_db):
    response = client.get(
        "/patient-name?dicom_filename=test/corrupt.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Error reading DICOM file"
