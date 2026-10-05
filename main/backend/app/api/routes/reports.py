"""Reports routes (stub)."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def status() -> dict:
    return {"module": "reports", "ready": False, "message": "stub"}
