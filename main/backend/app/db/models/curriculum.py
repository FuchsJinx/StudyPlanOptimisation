"""Curriculum plan models."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CurriculumPlan(Base):
    __tablename__ = "curriculum_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    study_year: Mapped[int] = mapped_column(Integer, nullable=False)
    education_form: Mapped[str] = mapped_column(String(5), nullable=False, default="О")
    source_plx_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_xlsx_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    import_status: Mapped[str] = mapped_column(String(20), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    disciplines: Mapped[list["PlanDiscipline"]] = relationship(back_populates="plan")


class PlanDiscipline(Base):
    __tablename__ = "plan_disciplines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("curriculum_plans.id"), nullable=False)
    discipline_name: Mapped[str] = mapped_column(String(255), nullable=False)
    cycle_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    hours_total: Mapped[float] = mapped_column(Float, default=0)
    hours_lec: Mapped[float] = mapped_column(Float, default=0)
    hours_prac: Mapped[float] = mapped_column(Float, default=0)
    hours_lab: Mapped[float] = mapped_column(Float, default=0)
    semester: Mapped[int | None] = mapped_column(Integer, nullable=True)

    plan: Mapped[CurriculumPlan] = relationship(back_populates="disciplines")
