"""Curriculum plan service stubs."""
from sqlalchemy.orm import Session

from app.db.models.curriculum import CurriculumPlan
from app.repositories.plans import PlanRepository


class PlanService:
    def __init__(self, db: Session):
        self.repo = PlanRepository(db)

    def list_plans(self, study_year: int | None = None) -> list[CurriculumPlan]:
        if study_year is not None:
            return self.repo.find_by_year(study_year)
        return self.repo.list(limit=500)

    def get_plan(self, plan_id: int) -> CurriculumPlan | None:
        return self.repo.get(plan_id)
