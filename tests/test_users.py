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
        "email": "test@example.com",
        "age": 25
    }

def test_create_user(test_user):
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    assert response.json()["name"] == test_user["name"]
    assert response.json()["email"] == test_user["email"]

def test_read_user(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == test_user["name"]

def test_read_users(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_user(test_user):
    # First create a user
    client.post("/users/", json=test_user)
    updated_data = {"name": "Updated Name", "email": "updated@example.com", "age": 26}
    response = client.put(f"/users/{test_user['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["email"] == updated_data["email"]

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
        "name": "Test User",
        "email": "invalid-email",  # Invalid email format
        "age": -1  # Invalid age
    }
    response = client.post("/users/", json=invalid_user)
    assert response.status_code == 422

def test_update_nonexistent_user():
    update_data = {"name": "Updated Name", "email": "updated@example.com", "age": 26}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404