import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token

client = TestClient(app)

# Dummy JWT token generation for authorization
@pytest.fixture(scope="module")
def token():
    # Generate a valid token for the test user
    return create_access_token(data={"sub": "testuser"})

def test_retrieve_patient_name_success(token):
    response = client.get(
        "/patient-name?dicom_filename=test/example.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "patient_name" in response.json()
    assert response.json()["patient_name"] == "John Doe"

def test_missing_dicom_file(token):
    response = client.get(
        "/patient-name?dicom_filename=missing.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "DICOM file not found"

def test_invalid_dicom_file(token):
    response = client.get(
        "/patient-name?dicom_filename=test/corrupt.dcm",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 500
    assert response.json()["detail"] == "Error reading DICOM file"
