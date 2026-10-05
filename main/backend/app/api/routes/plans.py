"""Curriculum plans routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas.plans import PlanOut
from app.services.plans import PlanService

router = APIRouter()


@router.get("", response_model=list[PlanOut])
def list_plans(study_year: int | None = None, db: Session = Depends(get_db)) -> list[PlanOut]:
    plans = PlanService(db).list_plans(study_year)
    return [PlanOut.model_validate(p) for p in plans]


@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: int, db: Session = Depends(get_db)) -> PlanOut:
    plan = PlanService(db).get_plan(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="План не найден")
    return PlanOut.model_validate(plan)
