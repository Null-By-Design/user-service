from api.model.domain import Address, User
from src.api.model.enum import UserRole, UserStatus
from src.api.model.schemas import HealthCheckResponse

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

user_minimal = User(
    id="123",
    username="testuser",
    email="test@example.com",
    created_at="2024-11-07T18:22:38.816855Z",
    updated_at="2024-11-07T18:22:38.816855Z",
)

user = User(
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
    created_at="2024-11-07T18:22:38.816855Z",
    updated_at="2024-11-07T18:22:38.816855Z",
)

address = Address(
    street="123 Test St",
    city="Test City",
    state="Test State",
    postal_code="12345",
    country="Test Country",
)


def get_user(address: Address) -> User:
    return User(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
        address=address,
        role=UserRole.GUEST,
        status=UserStatus.ACTIVE,
        created_at="2024-11-07T18:22:38.816855Z",
        updated_at="2024-11-07T18:22:38.816855Z",
    )


# REPOSITORY TEST DATA
save_user_dict = [
    {"id": 1},  # First fetch for address_id
    {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "address_id": 1,
        "role": "USER",
        "status": "ACTIVE",
        "last_login_at": None,
        "created_at": "2024-11-07T18:22:38.816855Z",
        "updated_at": "2024-11-07T18:22:38.816855Z",
    },
]
