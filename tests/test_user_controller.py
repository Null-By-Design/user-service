from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.api.controller.user_controller import router
from src.api.models.user import User

@pytest.fixture
def test_client():
    return TestClient(router)

@pytest.fixture
def mock_user_service():
    with patch("src.api.controller.user_controller.user_service") as mock:
        yield mock

def test_get_user_success(test_client, mock_user_service):
    user_id = 1
    mock_user_service.get_user.return_value = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        firstName="Test",
        lastName="User",
        phoneNumber="1234567890",
        address={"street": "123 Test St", "city": "Test City", "state": "TS", "country": "Testland", "postalCode": "12345"},
        role="user",
        status="active",
        lastLoginAt="2023-11-04T00:00:00",
        createdAt="2023-11-01T00:00:00",
        updatedAt="2023-11-01T00:00:00",
    )

    # Act
    response = test_client.get(f"/user/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "username": "testuser",
        "email": "test@example.com",
        "firstName": "Test",
        "lastName": "User",
        "phoneNumber": "1234567890",
        "address": {
            "street": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "country": "Testland",
            "postalCode": "12345"
        },
        "role": "user",
        "status": "active",
        "lastLoginAt": "2023-11-04T00:00:00",
        "createdAt": "2023-11-01T00:00:00",
        "updatedAt": "2023-11-01T00:00:00",
    }
    mock_user_service.get_user.assert_called_once_with(user_id)

def test_get_user_invalid_id(test_client):
    # Act
    response = test_client.get("/user/0")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Bad request, invalid user ID"}

def test_get_user_unauthorized(test_client, mock_user_service):
    # Arrange
    user_id = 1
    mock_user_service.get_user.return_value = None  # Simulate user not found

    with patch("src.api.controller.user_controller.is_authorized", return_value=False):
        # Act
        response = test_client.get(f"/user/{user_id}")

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized access"}

def test_get_user_not_found(test_client, mock_user_service):
    # Arrange
    user_id = 1
    mock_user_service.get_user.return_value = None  # Simulate user not found

    # Act
    response = test_client.get(f"/user/{user_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
