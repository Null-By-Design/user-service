from src.api.model.schemas import HealthCheckResponse
from src.api.repository import user_repository
from src.api.repository.user_repository import UserRepository


class HealthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def check_health(self):
        """
        Checks the health of the User Service, by attempting to connect to
        the configured database.

        Returns a HealthCheckResponse object, which contains the overall
        service status and a dictionary of dependencies and their status.

        A "Healthy" status indicates that all dependencies are connected
        and available. An "Unhealthy" status means that one or more
        dependencies are not available.
        """
        response = HealthCheckResponse(status="Healthy")
        dependencies = {
            "database": self.user_repository.check_db_connection(),
        }
        for name, status in dependencies.items():
            if status != "Connected":
                response.status = "Unhealthy"
            response.add_detail(name, status)
        return response
