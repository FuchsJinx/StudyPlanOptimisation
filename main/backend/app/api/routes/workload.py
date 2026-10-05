"""Workload routes (stub)."""
from fastapi import APIRouter

from app.schemas.common import ModuleStatus
from app.services.workload import WorkloadService

router = APIRouter()


@router.get("/status", response_model=ModuleStatus)
def status() -> ModuleStatus:
    return ModuleStatus(**WorkloadService().status())
