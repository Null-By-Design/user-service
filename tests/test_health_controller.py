from unittest.mock import Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.controller.health_controller import router
from src.api.dependencies.provider import get_health_service
from src.api.service.health_service import HealthService
from tests.test_data import (
    health_check_db_error_response,
    health_check_db_error_response_json,
    health_check_valid_response_json,
    health_check_valid_service_response,
)


# Test fixtures
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_health_service():
    return Mock(spec=HealthService)


@pytest.fixture
def mock_get_health_service(mock_health_service):
    return lambda: mock_health_service


def test_get_health_status_ok(
    app, client, mock_health_service, mock_get_health_service
):
    # Override the dependency
    app.dependency_overrides[get_health_service] = mock_get_health_service

    mock_health_service.check_health.return_value = health_check_valid_service_response

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == health_check_valid_response_json
    mock_health_service.check_health.assert_called_once()


def test_get_health_status_error(
    app, client, mock_health_service, mock_get_health_service
):
    # Override the dependency
    app.dependency_overrides[get_health_service] = mock_get_health_service

    mock_health_service.check_health.return_value = health_check_db_error_response

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == health_check_db_error_response_json
    mock_health_service.check_health.assert_called_once()
