from src.api.model.schemas import HealthCheckResponse
from src.api.model.user import User

# HEALTH TEST DATA
health_check_valid_service_response = HealthCheckResponse(status="OK")
health_check_valid_service_response.add_detail("database", "Connected")

health_check_db_error_response = HealthCheckResponse(status="ERROR")
health_check_db_error_response.add_detail("database", "Failed to connect")

health_check_valid_response_json = {
    "status": "OK",
    "dependencies": {"database": "Connected"},
}

health_check_db_error_response_json = {
    "status": "ERROR",
    "dependencies": {"database": "Failed to connect"},
}

# USER TEST DATA
user_request_valid_json = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
}

user_request_bad_email_json = {
    "username": "username",
    "email": "invalid-email",  # Invalid email format
    "password": "123",
}

user_request_no_email_phone_no_json = {
    "username": "username",
    "password": "123",
}

user_response_valid_json = """{"id":123,"username":"testuser","email":"test@example.com","firstName":null,"lastName":null,"phoneNumber":null,"address":null,"role":"GUEST","status":"ACTIVE","lastLoginAt":null,"createdAt":"2024-11-07T18:22:38.816855Z","updatedAt":"2024-11-07T18:22:38.816855Z"}"""

user_valid = User(
    id="123",
    username="testuser",
    email="test@example.com",
    created_at="2024-11-07T18:22:38.816855Z",
    updated_at="2024-11-07T18:22:38.816855Z",
)
