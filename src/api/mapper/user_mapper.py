from src.api.model.address import Address
from src.api.model.schemas import Address as UserRegistrationRequestAddress
from src.api.model.schemas import UserRegistrationRequest, UserResponse
from src.api.model.user import User


class UserMapper:
    @staticmethod
    def to_domain(request: UserRegistrationRequest) -> User:
        """
        Maps a UserRegistrationRequest object to a User object.

        Args:
            request (UserRegistrationRequest): The request to map.

        Returns:
            User: The mapped User object.
        """
        address = (
            None
            if request.address is None
            else Address(
                street=request.address.street,
                city=request.address.city,
                state=request.address.state,
                country=request.address.country,
                postal_code=request.address.postalCode,
            )
        )
        return User(
            username=request.username,
            email=request.email,
            first_name=request.firstName,
            last_name=request.lastName,
            phone_number=request.phoneNumber,
            address=address,
            role=request.role,
            status=request.status,
        )

    @staticmethod
    def to_response(user: User) -> UserResponse:
        """
        Maps a User object to a UserResponse object.

        Args:
            user (User): The user to map.

        Returns:
            UserResponse: The mapped UserResponse object.
        """
        address = (
            None
            if user.address is None
            else UserRegistrationRequestAddress(
                street=user.address.street,
                city=user.address.city,
                state=user.address.state,
                country=user.address.country,
                postalCode=user.address.postal_code,
            )
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            firstName=user.first_name,
            lastName=user.last_name,
            phoneNumber=user.phone_number,
            address=address,
            role=user.role,
            status=user.status,
            lastLoginAt=user.last_login_at,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
        )

    @staticmethod
    def build_user_object(user: dict, address: Address) -> User:
        """
        Builds a User object from a dictionary and an Address object.

        Args:
            user (dict): A dictionary containing user attributes.
            address (Address): An Address object associated with the user.

        Returns:
            User: A User object constructed from the provided data.
        """
        return User(
            id=user["id"],
            username=user["username"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            phone_number=user["phone_number"],
            address=address,
            role=user["role"],
            status=user["status"],
            last_login_at=user["last_login_at"],
            created_at=user["created_at"],
            updated_at=user["updated_at"],
        )
