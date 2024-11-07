from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from psycopg2 import errors

from src.api.model.address import Address
from src.api.model.user import User
from src.api.repository.user_repository import UserRepository
from src.api.service.user_service import UserService


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(mock_user_repository)


@pytest.fixture
def mock_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
        address=Address(
            street="123 Main St",
            city="Anytown",
            state="CA",
            postal_code="12345",
            country="USA",
        ),
        role="user",
        status="active",
        created_at="2023-04-01T12:00:00",
        updated_at="2023-04-01T12:00:00",
    )


@pytest.mark.asyncio
async def test_register_user_success(user_service, mock_user_repository, mock_user):
    mock_user_repository.save.return_value = mock_user

    registered_user = await user_service.register_user(mock_user)

    assert registered_user == mock_user
    mock_user_repository.save.assert_called_once_with(mock_user)


@pytest.mark.asyncio
async def test_register_user_failed(user_service, mock_user_repository, mock_user):
    mock_user_repository.save.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await user_service.register_user(mock_user)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Failed to create user"
    mock_user_repository.save.assert_called_once_with(mock_user)


@pytest.mark.asyncio
async def test_register_user_exception(user_service, mock_user_repository, mock_user):
    mock_user_repository.save.side_effect = Exception("Database error")

    with pytest.raises(HTTPException) as exc_info:
        await user_service.register_user(mock_user)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error"
    mock_user_repository.save.assert_called_once_with(mock_user)


@pytest.mark.asyncio
async def test_register_user_record_exists(
    user_service, mock_user_repository, mock_user
):
    mock_user_repository.save.side_effect = errors.UniqueViolation(
        "User already exists"
    )

    with pytest.raises(HTTPException) as exc_info:
        await user_service.register_user(mock_user)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "User already exists"
    mock_user_repository.save.assert_called_once_with(mock_user)
