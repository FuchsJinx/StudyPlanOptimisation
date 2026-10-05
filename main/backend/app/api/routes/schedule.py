"""Schedule routes (stub)."""
from fastapi import APIRouter

from app.schemas.common import ModuleStatus
from app.services.schedule import ScheduleService

router = APIRouter()


@router.get("/status", response_model=ModuleStatus)
def status() -> ModuleStatus:
    return ModuleStatus(**ScheduleService().status())
