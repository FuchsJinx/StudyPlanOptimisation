"""Repositories for reference directories."""
from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.models.refs import Classroom, LessonType, Specialty, StudyGroup, Subject, Teacher


class RefsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def summary(self) -> dict[str, int]:
        return {
            "groups": self.db.scalar(select(func.count()).select_from(StudyGroup)) or 0,
            "teachers": self.db.scalar(select(func.count()).select_from(Teacher)) or 0,
            "classrooms": self.db.scalar(select(func.count()).select_from(Classroom)) or 0,
            "subjects": self.db.scalar(select(func.count()).select_from(Subject)) or 0,
            "specialties": self.db.scalar(select(func.count()).select_from(Specialty)) or 0,
            "lesson_types": self.db.scalar(select(func.count()).select_from(LessonType)) or 0,
        }

    def list_groups(self) -> list[StudyGroup]:
        return list(self.db.scalars(select(StudyGroup).order_by(StudyGroup.code)).all())

    def get_group(self, item_id: int) -> StudyGroup | None:
        return self.db.get(StudyGroup, item_id)

    def get_group_by_code(self, code: str) -> StudyGroup | None:
        return self.db.scalar(select(StudyGroup).where(StudyGroup.code == code))

    def add_group(self, item: StudyGroup) -> StudyGroup:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def save(self, item: object) -> object:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: object) -> None:
        self.db.delete(item)
        self.db.commit()

    def list_teachers(self) -> list[Teacher]:
        return list(self.db.scalars(select(Teacher).order_by(Teacher.full_name)).all())

    def get_teacher(self, item_id: int) -> Teacher | None:
        return self.db.get(Teacher, item_id)

    def list_classrooms(self) -> list[Classroom]:
        return list(self.db.scalars(select(Classroom).order_by(Classroom.code)).all())

    def get_classroom(self, item_id: int) -> Classroom | None:
        return self.db.get(Classroom, item_id)

    def get_classroom_by_code(self, code: str) -> Classroom | None:
        return self.db.scalar(select(Classroom).where(Classroom.code == code))

    def list_subjects(self) -> list[Subject]:
        return list(self.db.scalars(select(Subject).order_by(Subject.code)).all())

    def get_subject(self, item_id: int) -> Subject | None:
        return self.db.get(Subject, item_id)

    def get_subject_by_code(self, code: str) -> Subject | None:
        return self.db.scalar(select(Subject).where(Subject.code == code))

    def list_specialties(self) -> list[Specialty]:
        return list(self.db.scalars(select(Specialty).order_by(Specialty.code)).all())

    def get_specialty(self, item_id: int) -> Specialty | None:
        return self.db.get(Specialty, item_id)

    def get_specialty_by_code(self, code: str) -> Specialty | None:
        return self.db.scalar(select(Specialty).where(Specialty.code == code))

    def list_lesson_types(self) -> list[LessonType]:
        return list(self.db.scalars(select(LessonType).order_by(LessonType.code)).all())

    def get_lesson_type(self, item_id: int) -> LessonType | None:
        return self.db.get(LessonType, item_id)

    def get_lesson_type_by_code(self, code: str) -> LessonType | None:
        return self.db.scalar(select(LessonType).where(LessonType.code == code))
