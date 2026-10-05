"""Root API router."""
from fastapi import APIRouter

from app.api.routes import (
    admin,
    auth,
    health,
    journal,
    plans,
    reports,
    schedule,
    substitutions,
    workload,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(workload.router, prefix="/workload", tags=["workload"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(substitutions.router, prefix="/substitutions", tags=["substitutions"])
api_router.include_router(journal.router, prefix="/journal", tags=["journal"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
