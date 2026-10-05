"""Admin routes (stub)."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def status() -> dict:
    return {"module": "admin", "ready": False, "message": "stub"}
