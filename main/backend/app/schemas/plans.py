"""Curriculum plan schemas."""
from datetime import datetime

from app.schemas.common import ORMModel


class PlanOut(ORMModel):
    id: int
    code: str | None = None
    title: str
    study_year: int
    education_form: str
    import_status: str
    created_at: datetime | None = None
