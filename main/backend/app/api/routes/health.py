"""Health endpoint."""
from fastapi import APIRouter

from app.schemas.common import HealthResponse
from app.services.health import health_payload

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(**health_payload())
