"""Journal routes (stub)."""
from fastapi import APIRouter

from app.schemas.common import ModuleStatus
from app.services.journal import JournalService

router = APIRouter()


@router.get("/status", response_model=ModuleStatus)
def status() -> ModuleStatus:
    return ModuleStatus(**JournalService().status())
