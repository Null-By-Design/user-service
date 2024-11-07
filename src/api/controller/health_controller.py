from fastapi import APIRouter, Depends

from src.api.dependencies.provider import get_health_service
from src.api.model.schemas import HealthCheckResponse
from src.api.service.health_service import HealthService

router = APIRouter()


@router.get("/health")
def get_health_status(
    health_service: HealthService = Depends(get_health_service),
) -> HealthCheckResponse:
    return health_service.check_health()
