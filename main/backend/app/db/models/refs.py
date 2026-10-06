"""Reference dictionaries: groups, teachers, classrooms, subjects."""
from sqlalchemy import Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    budget_flag: Mapped[int] = mapped_column(Integer, default=1)
    contacts: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, default=1)


class StudyGroup(Base):
    __tablename__ = "study_groups"
    __table_args__ = (UniqueConstraint("code", name="uq_study_groups_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    education_form: Mapped[str] = mapped_column(String(5), default="О")
    specialty_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    study_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, default=1)


class Classroom(Base):
    __tablename__ = "classrooms"
    __table_args__ = (UniqueConstraint("code", name="uq_classrooms_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    building: Mapped[str | None] = mapped_column(String(50), nullable=True)
    room_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, default=1)


class Subject(Base):
    __tablename__ = "subjects"
    __table_args__ = (UniqueConstraint("code", name="uq_subjects_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    short_title: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cycle: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[int] = mapped_column(Integer, default=1)



class Specialty(Base):
    __tablename__ = "specialties"
    __table_args__ = (UniqueConstraint("code", name="uq_specialties_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1)


class LessonType(Base):
    __tablename__ = "lesson_types"
    __table_args__ = (UniqueConstraint("code", name="uq_lesson_types_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(30), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
