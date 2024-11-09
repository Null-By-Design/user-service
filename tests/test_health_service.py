from unittest.mock import MagicMock

import pytest

from src.api.dependencies.provider import get_health_service
from src.api.model.schemas import HealthCheckResponse
from src.api.repository.user_repository import UserRepository
from src.api.service.health_service import HealthService


@pytest.fixture
def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def health_service(mock_user_repository):
    return HealthService(mock_user_repository)


def test_check_health_all_ok(health_service, mock_user_repository):
    mock_user_repository.check_db_connection.return_value = "Connected"

    response = health_service.check_health()

    assert isinstance(response, HealthCheckResponse)
    assert response.status == "Healthy"
    assert response.dependencies == {"database": "Connected"}


def test_check_health_database_error(health_service, mock_user_repository):
    mock_user_repository.check_db_connection.return_value = "Failed to connect"

    response = health_service.check_health()

    assert isinstance(response, HealthCheckResponse)
    assert response.status == "Unhealthy"
    assert response.dependencies == {"database": "Failed to connect"}
