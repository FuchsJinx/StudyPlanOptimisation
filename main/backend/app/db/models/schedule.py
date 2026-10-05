"""Schedule and substitution models."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduleSlot(Base):
    __tablename__ = "schedule_slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("study_groups.id"), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    classroom_id: Mapped[int | None] = mapped_column(ForeignKey("classrooms.id"), nullable=True)
    discipline_name: Mapped[str] = mapped_column(String(255), nullable=False)
    week_day: Mapped[int] = mapped_column(Integer, nullable=False)
    pair_number: Mapped[int] = mapped_column(Integer, nullable=False)
    week_type: Mapped[str] = mapped_column(String(10), default="all")
    status: Mapped[str] = mapped_column(String(20), default="planned")


class Substitution(Base):
    __tablename__ = "substitutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("schedule_slots.id"), nullable=False)
    subst_type: Mapped[str] = mapped_column(String(30), nullable=False)
    new_teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    new_week_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    new_pair_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
