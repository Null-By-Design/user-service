from fastapi import Depends
from typing import Dict

from src.api.repository.user_repository import UserRepository
from src.api.service.user_service import UserService
from src.api.service.health_service import HealthService


class Providers:
    _instances: Dict = {}

    @staticmethod
    def get_user_repository() -> UserRepository:
        """
        Singleton provider for UserRepository
        """
        if UserRepository not in Providers._instances:
            Providers._instances[UserRepository] = UserRepository()
        return Providers._instances[UserRepository]

    @staticmethod
    def get_user_service(
        user_repository: UserRepository = Depends(get_user_repository),
    ) -> UserService:
        """
        Provider for UserService with repository dependency
        """
        if UserService not in Providers._instances:
            Providers._instances[UserService] = UserService(user_repository)
        return Providers._instances[UserService]

    @staticmethod
    def get_health_service(
        user_repository: UserRepository = Depends(get_user_repository),
    ) -> HealthService:
        """
        Provider for HealthService with repository dependency
        """
        if HealthService not in Providers._instances:
            Providers._instances[HealthService] = HealthService(user_repository)
        return Providers._instances[HealthService]


# FastAPI dependency injection functions
def get_user_repository() -> UserRepository:
    return Providers.get_user_repository()


def get_health_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> HealthService:
    """
    FastAPI dependency for HealthService
    """
    return Providers.get_health_service(user_repository)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    """
    FastAPI dependency for UserService
    """
    return Providers.get_user_service(user_repository)
