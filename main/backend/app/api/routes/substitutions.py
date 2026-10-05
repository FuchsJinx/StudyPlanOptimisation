"""Substitutions routes (stub)."""
from fastapi import APIRouter

from app.schemas.common import ModuleStatus
from app.services.substitution import SubstitutionService

router = APIRouter()


@router.get("/status", response_model=ModuleStatus)
def status() -> ModuleStatus:
    return ModuleStatus(**SubstitutionService().status())
