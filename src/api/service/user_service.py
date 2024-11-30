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

    async def get_user(self, user_id: int) -> User:
        """
        Fetch a user by their ID.

        Args:
            user_id (int): The ID of the user to fetch.

        Returns:
            User: The user with the given ID.

        Raises:
            HTTPException: If the user cannot be found (404).
        """
        try:
            user = self.user_repository.get_user(user_id)  # This should trigger the mock
            if user is None:
                # Raise an exception if user not found
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return user
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching user: {str(e)}",
            )
            
    async def update_user(self, user_id: int, updated_user_data: User) -> User:
        """
        Update an existing user by their ID.

        Args:
            user_id (int): The ID of the user to update.
            updated_user_data (User): The new user data.

        Returns:
            User: The updated user.

        Raises:
            HTTPException: If the update fails (500) or the user is not found (404).
        """
        try:
            # Check if the user exists
            existing_user = self.user_repository.get_user(user_id)
            if not existing_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            # Update the user using the repository
            updated_user = self.user_repository.update_user(user_id, updated_user_data)
            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to update user",
                )
            return updated_user
        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating user: {str(e)}",
            )

