from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from psycopg2 import errors

from src.api.repository.user_repository import UserRepository
from src.api.service.user_service import UserService
from tests.test_data import user


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    return UserService(mock_user_repository)


@pytest.fixture
def mock_user():
    return user


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
    assert exc_info.value.detail == "500: Failed to create user"
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
