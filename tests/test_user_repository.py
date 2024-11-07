from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi import HTTPException, status
from psycopg2 import errors

from src.api.repository.user_repository import UserRepository
from tests.test_data import address, get_user, save_user_dict


# Test fixtures
@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def mock_db_cursor():
    cursor = MagicMock()
    cursor.__enter__ = Mock(return_value=cursor)
    cursor.__exit__ = Mock(return_value=None)
    return cursor


@pytest.fixture
def mock_db_connection(mock_db_cursor):
    connection = MagicMock()
    connection.__enter__ = Mock(return_value=connection)
    connection.__exit__ = Mock(return_value=None)
    connection.cursor.return_value = mock_db_cursor
    return connection


@pytest.fixture
def mock_db_pool(mock_db_connection):
    with patch(
        "src.api.config.database.DatabasePool.get_connection"
    ) as mock_get_connection:
        mock_get_connection.return_value.__enter__.return_value = mock_db_connection
        yield mock_get_connection


@pytest.fixture
def sample_address():
    return address


@pytest.fixture
def sample_user(sample_address):
    return get_user(sample_address)


def test_check_db_connection_success(user_repository, mock_db_pool):
    # Arrange
    mock_cursor = MagicMock()
    mock_cursor.__enter__.return_value = mock_cursor
    mock_cursor.__exit__.return_value = None
    mock_db_pool.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    # Set execute method to ensure it works as expected
    mock_cursor.execute.return_value = None

    # Act
    result = user_repository.check_db_connection()

    # Assert
    assert result == "Connected"
    mock_cursor.execute.assert_called_once_with("SELECT 1")


def test_check_db_connection_failure(user_repository, mock_db_pool):
    # Arrange
    mock_cursor = MagicMock()
    mock_cursor.__enter__.side_effect = Exception("Connection failed")

    # Make sure that when get_connection is called, it returns a mock connection with our mock cursor
    mock_db_pool.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    # Act
    result = user_repository.check_db_connection()

    # Assert
    assert "Failed to connect to database" in result
    assert "Connection failed" in result


# Tests for save method
def test_save_user_success(
    user_repository, mock_db_pool, mock_db_connection, mock_db_cursor, sample_user
):
    # Arrange
    mock_db_pool.get_connection.return_value = mock_db_connection

    # Mock insertion
    mock_db_cursor.fetchone.side_effect = save_user_dict

    # Act
    result = user_repository.save(sample_user)

    # Assert
    assert result is not None
    assert result.username == sample_user.username
    assert result.email == sample_user.email
    mock_db_connection.commit.assert_called_once()


def test_save_user_unique_violation(
    user_repository, mock_db_pool, mock_db_connection, mock_db_cursor, sample_user
):
    # Arrange
    mock_db_pool.get_connection.return_value = mock_db_connection
    mock_db_cursor.execute.side_effect = errors.UniqueViolation("Duplicate user")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        user_repository.save(sample_user)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert "User already exists" in str(exc_info.value.detail)
