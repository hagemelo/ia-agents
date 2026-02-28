from fastapi import APIRouter
from health_service import HealthService

router = APIRouter(prefix="/health", tags=["Health"])

service = HealthService()

@router.get("/live")
def liveness():
    return service.liveness()