"""Workload assignment model."""
from sqlalchemy import ForeignKey, Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkloadAssignment(Base):
    __tablename__ = "workload_assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_discipline_id: Mapped[int] = mapped_column(ForeignKey("plan_disciplines.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("study_groups.id"), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    lesson_type: Mapped[str] = mapped_column(String(20), nullable=False, default="lec")
    hours_plan: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    hours_share: Mapped[float] = mapped_column(Float, default=1.0)
    status: Mapped[str] = mapped_column(String(20), default="assigned")
