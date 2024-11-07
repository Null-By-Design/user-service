from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from src.api.controller.user_controller import router
from src.api.dependencies.provider import get_user_service
from src.api.service.user_service import UserService
from tests.test_data import (
    user_request_bad_email_json,
    user_request_no_email_phone_no_json,
    user_request_valid_json,
    user_response_valid_json,
    user_valid,
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
def mock_user_service():
    return Mock(spec=UserService)


@pytest.fixture
def mock_get_user_service(mock_user_service):
    return lambda: mock_user_service


# Test data fixtures
@pytest.fixture
def valid_user_request():
    return user_request_valid_json


@pytest.fixture
def valid_user_service_response():
    return user_valid


@pytest.mark.asyncio
async def test_register_user_success(
    app,
    client,
    mock_user_service,
    mock_get_user_service,
    valid_user_request,
    valid_user_service_response,
):
    # Override the dependency
    app.dependency_overrides[get_user_service] = mock_get_user_service

    # Setup mock response
    mock_user_service.register_user = AsyncMock(
        return_value=valid_user_service_response
    )

    # Make request
    response = client.post("/api/v1/user", json=valid_user_request)

    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content.decode() == user_response_valid_json
    mock_user_service.register_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_user_invalid_email(
    app, client, mock_user_service, mock_get_user_service
):
    # Override the dependency
    app.dependency_overrides[get_user_service] = mock_get_user_service

    # Invalid request data

    # Make request
    response = client.post("/api/v1/user", json=user_request_bad_email_json)

    # Assertions
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    mock_user_service.register_user.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_no_email_phone_number(
    app, client, mock_user_service, mock_get_user_service
):
    # Override the dependency
    app.dependency_overrides[get_user_service] = mock_get_user_service

    # Make request
    response = client.post("/api/v1/user", json=user_request_no_email_phone_no_json)

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    mock_user_service.register_user.assert_not_called()


@pytest.mark.asyncio
async def test_register_user_http_exception(
    app, client, mock_user_service, mock_get_user_service, valid_user_request
):
    # Override the dependency
    app.dependency_overrides[get_user_service] = mock_get_user_service

    # Setup mock to raise HTTPException
    from fastapi import HTTPException

    mock_user_service.register_user = AsyncMock(
        side_effect=HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    )

    # Make request
    response = client.post("/api/v1/user", json=valid_user_request)

    # Assertions
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "User already exists"
    mock_user_service.register_user.assert_called_once()


# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup(app):
    yield
    app.dependency_overrides.clear()
