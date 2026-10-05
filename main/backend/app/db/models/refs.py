"""Reference dictionaries."""
from sqlalchemy import Integer, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    budget_flag: Mapped[int] = mapped_column(Integer, default=1)
    contacts: Mapped[str | None] = mapped_column(String(255), nullable=True)


class StudyGroup(Base):
    __tablename__ = "study_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    education_form: Mapped[str] = mapped_column(String(5), default="О")
    specialty_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    study_year: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    building: Mapped[str | None] = mapped_column(String(50), nullable=True)
