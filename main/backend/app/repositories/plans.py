"""Curriculum plan repository."""
from sqlalchemy.orm import Session

from app.db.models.curriculum import CurriculumPlan
from app.repositories.base import BaseRepository


class PlanRepository(BaseRepository[CurriculumPlan]):
    def __init__(self, db: Session):
        super().__init__(db, CurriculumPlan)

    def find_by_year(self, study_year: int) -> list[CurriculumPlan]:
        return list(
            self.db.query(CurriculumPlan)
            .filter(CurriculumPlan.study_year == study_year)
            .order_by(CurriculumPlan.title)
            .all()
        )
