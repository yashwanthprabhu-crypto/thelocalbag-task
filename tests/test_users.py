import pytest
from fastapi.testclient import TestClient
from main import app
from models import User

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "id": 1,
        "name": "Test User",
        "phone_no": "+919876543210",
        "address": "123 Test Street, Test City"
    }

def test_create_user(test_user):
    response = client.post("/users/", json=test_user)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"

def test_read_user(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == test_user["name"]
    assert response.json()["phone_no"] == test_user["phone_no"]

def test_read_users(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_user(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    updated_data = {
        "id": test_user["id"],
        "name": "Updated Name",
        "phone_no": "+919876543211",
        "address": "456 Updated Street, Updated City"
    }
    response = client.put(f"/users/{test_user['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"

def test_delete_user(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    response = client.delete(f"/users/{test_user['id']}")
    assert response.status_code == 200
    # Verify user is deleted
    get_response = client.get(f"/users/{test_user['id']}")
    assert get_response.status_code == 404

def test_create_user_invalid_data():
    invalid_user = {
        "id": 1,
        "name": "Test123",  # Invalid name with numbers
        "phone_no": "invalid-phone",  # Invalid phone format
        "address": ""  # Empty address
    }
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422

def test_update_nonexistent_user():
    update_data = {
        "id": 999,
        "name": "Updated Name",
        "phone_no": "+919876543211",
        "address": "456 Updated Street, Updated City"
    }
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404