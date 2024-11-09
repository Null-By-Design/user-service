from fastapi import HTTPException, status

from src.api.model.domain import User
from src.api.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user: User) -> User:
        """
        Registers a new user.

        Args:
            user (User): The user to register.

        Returns:
            User: The registered user.

        Raises:
            HTTPException: If the user cannot be registered (500).
        """

        try:
            saved_user = self.user_repository.save(user)
            if not saved_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user",
                )
            return saved_user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
