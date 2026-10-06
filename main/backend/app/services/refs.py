"""Business logic for reference directories."""
from __future__ import annotations

from fastapi import HTTPException, status

from app.db.models.refs import Classroom, LessonType, Specialty, StudyGroup, Subject, Teacher
from app.repositories.refs import RefsRepository
from app.schemas.refs import (
    ClassroomCreate,
    ClassroomOut,
    ClassroomUpdate,
    DirectorySummary,
    LessonTypeCreate,
    LessonTypeOut,
    LessonTypeUpdate,
    SpecialtyCreate,
    SpecialtyOut,
    SpecialtyUpdate,
    StudyGroupCreate,
    StudyGroupOut,
    StudyGroupUpdate,
    SubjectCreate,
    SubjectOut,
    SubjectUpdate,
    TeacherCreate,
    TeacherOut,
    TeacherUpdate,
)


def _flag(value: int | bool | None, default: bool = True) -> bool:
    if value is None:
        return default
    return bool(int(value)) if not isinstance(value, bool) else value


def group_out(item: StudyGroup) -> StudyGroupOut:
    return StudyGroupOut(
        id=item.id,
        code=item.code,
        size=item.size,
        education_form=item.education_form,
        specialty_code=item.specialty_code,
        study_year=item.study_year,
        is_active=_flag(item.is_active),
    )


def teacher_out(item: Teacher) -> TeacherOut:
    return TeacherOut(
        id=item.id,
        full_name=item.full_name,
        rate=item.rate,
        budget_flag=_flag(item.budget_flag),
        contacts=item.contacts,
        is_active=_flag(item.is_active),
    )


def classroom_out(item: Classroom) -> ClassroomOut:
    return ClassroomOut(
        id=item.id,
        code=item.code,
        capacity=item.capacity,
        building=item.building,
        room_type=item.room_type,
        is_active=_flag(item.is_active),
    )


def subject_out(item: Subject) -> SubjectOut:
    return SubjectOut(
        id=item.id,
        code=item.code,
        title=item.title,
        short_title=item.short_title,
        cycle=item.cycle,
        is_active=_flag(item.is_active),
    )


class RefsService:
    def __init__(self, db) -> None:
        self.repo = RefsRepository(db)

    def summary(self) -> DirectorySummary:
        return DirectorySummary(**self.repo.summary())

    # ---- groups ----
    def list_groups(self) -> list[StudyGroupOut]:
        return [group_out(x) for x in self.repo.list_groups()]

    def create_group(self, body: StudyGroupCreate) -> StudyGroupOut:
        code = body.code.strip()
        if self.repo.get_group_by_code(code):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Группа с таким кодом уже есть")
        item = StudyGroup(
            code=code,
            size=body.size,
            education_form=body.education_form.strip() or "О",
            specialty_code=body.specialty_code,
            study_year=body.study_year,
            is_active=1,
        )
        return group_out(self.repo.add_group(item))

    def update_group(self, item_id: int, body: StudyGroupUpdate) -> StudyGroupOut:
        item = self.repo.get_group(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
        data = body.model_dump(exclude_unset=True)
        if "code" in data and data["code"] is not None:
            code = data["code"].strip()
            other = self.repo.get_group_by_code(code)
            if other and other.id != item.id:
                raise HTTPException(status.HTTP_409_CONFLICT, detail="Группа с таким кодом уже есть")
            item.code = code
        if "size" in data:
            item.size = data["size"]
        if "education_form" in data and data["education_form"] is not None:
            item.education_form = data["education_form"].strip() or "О"
        if "specialty_code" in data:
            item.specialty_code = data["specialty_code"]
        if "study_year" in data:
            item.study_year = data["study_year"]
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        return group_out(self.repo.save(item))  # type: ignore[arg-type]

    def delete_group(self, item_id: int) -> None:
        item = self.repo.get_group(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
        self.repo.delete(item)

    # ---- teachers ----
    def list_teachers(self) -> list[TeacherOut]:
        return [teacher_out(x) for x in self.repo.list_teachers()]

    def create_teacher(self, body: TeacherCreate) -> TeacherOut:
        item = Teacher(
            full_name=body.full_name.strip(),
            rate=body.rate,
            budget_flag=1 if body.budget_flag else 0,
            contacts=body.contacts,
            is_active=1,
        )
        return teacher_out(self.repo.save(item))  # type: ignore[arg-type]

    def update_teacher(self, item_id: int, body: TeacherUpdate) -> TeacherOut:
        item = self.repo.get_teacher(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")
        data = body.model_dump(exclude_unset=True)
        if "full_name" in data and data["full_name"] is not None:
            item.full_name = data["full_name"].strip()
        if "rate" in data:
            item.rate = data["rate"]
        if "budget_flag" in data and data["budget_flag"] is not None:
            item.budget_flag = 1 if data["budget_flag"] else 0
        if "contacts" in data:
            item.contacts = data["contacts"]
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        return teacher_out(self.repo.save(item))  # type: ignore[arg-type]

    def delete_teacher(self, item_id: int) -> None:
        item = self.repo.get_teacher(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")
        self.repo.delete(item)

    # ---- classrooms ----
    def list_classrooms(self) -> list[ClassroomOut]:
        return [classroom_out(x) for x in self.repo.list_classrooms()]

    def create_classroom(self, body: ClassroomCreate) -> ClassroomOut:
        code = body.code.strip()
        if self.repo.get_classroom_by_code(code):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Кабинет с таким кодом уже есть")
        item = Classroom(
            code=code,
            capacity=body.capacity,
            building=body.building,
            room_type=body.room_type,
            is_active=1,
        )
        return classroom_out(self.repo.save(item))  # type: ignore[arg-type]

    def update_classroom(self, item_id: int, body: ClassroomUpdate) -> ClassroomOut:
        item = self.repo.get_classroom(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Кабинет не найден")
        data = body.model_dump(exclude_unset=True)
        if "code" in data and data["code"] is not None:
            code = data["code"].strip()
            other = self.repo.get_classroom_by_code(code)
            if other and other.id != item.id:
                raise HTTPException(status.HTTP_409_CONFLICT, detail="Кабинет с таким кодом уже есть")
            item.code = code
        if "capacity" in data:
            item.capacity = data["capacity"]
        if "building" in data:
            item.building = data["building"]
        if "room_type" in data:
            item.room_type = data["room_type"]
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        return classroom_out(self.repo.save(item))  # type: ignore[arg-type]

    def delete_classroom(self, item_id: int) -> None:
        item = self.repo.get_classroom(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Кабинет не найден")
        self.repo.delete(item)

    # ---- subjects ----
    def list_subjects(self) -> list[SubjectOut]:
        return [subject_out(x) for x in self.repo.list_subjects()]

    def create_subject(self, body: SubjectCreate) -> SubjectOut:
        code = body.code.strip()
        if self.repo.get_subject_by_code(code):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Предмет с таким кодом уже есть")
        item = Subject(
            code=code,
            title=body.title.strip(),
            short_title=body.short_title,
            cycle=body.cycle,
            is_active=1,
        )
        return subject_out(self.repo.save(item))  # type: ignore[arg-type]

    def update_subject(self, item_id: int, body: SubjectUpdate) -> SubjectOut:
        item = self.repo.get_subject(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
        data = body.model_dump(exclude_unset=True)
        if "code" in data and data["code"] is not None:
            code = data["code"].strip()
            other = self.repo.get_subject_by_code(code)
            if other and other.id != item.id:
                raise HTTPException(status.HTTP_409_CONFLICT, detail="Предмет с таким кодом уже есть")
            item.code = code
        if "title" in data and data["title"] is not None:
            item.title = data["title"].strip()
        if "short_title" in data:
            item.short_title = data["short_title"]
        if "cycle" in data:
            item.cycle = data["cycle"]
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        return subject_out(self.repo.save(item))  # type: ignore[arg-type]

    def delete_subject(self, item_id: int) -> None:
        item = self.repo.get_subject(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
        self.repo.delete(item)

    # ---- specialties ----
    def list_specialties(self) -> list[SpecialtyOut]:
        return [
            SpecialtyOut(id=x.id, code=x.code, title=x.title, is_active=_flag(x.is_active))
            for x in self.repo.list_specialties()
        ]

    def create_specialty(self, body: SpecialtyCreate) -> SpecialtyOut:
        code = body.code.strip()
        if self.repo.get_specialty_by_code(code):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Специальность с таким кодом уже есть")
        item = Specialty(code=code, title=body.title.strip(), is_active=1)
        saved = self.repo.save(item)
        return SpecialtyOut(id=saved.id, code=saved.code, title=saved.title, is_active=True)  # type: ignore[attr-defined]

    def update_specialty(self, item_id: int, body: SpecialtyUpdate) -> SpecialtyOut:
        item = self.repo.get_specialty(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Специальность не найдена")
        data = body.model_dump(exclude_unset=True)
        if "code" in data and data["code"] is not None:
            code = data["code"].strip()
            other = self.repo.get_specialty_by_code(code)
            if other and other.id != item.id:
                raise HTTPException(status.HTTP_409_CONFLICT, detail="Специальность с таким кодом уже есть")
            item.code = code
        if "title" in data and data["title"] is not None:
            item.title = data["title"].strip()
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        saved = self.repo.save(item)
        return SpecialtyOut(
            id=saved.id,  # type: ignore[attr-defined]
            code=saved.code,  # type: ignore[attr-defined]
            title=saved.title,  # type: ignore[attr-defined]
            is_active=_flag(saved.is_active),  # type: ignore[attr-defined]
        )

    def delete_specialty(self, item_id: int) -> None:
        item = self.repo.get_specialty(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Специальность не найдена")
        self.repo.delete(item)

    # ---- lesson types ----
    def list_lesson_types(self) -> list[LessonTypeOut]:
        return [
            LessonTypeOut(id=x.id, code=x.code, title=x.title, is_active=_flag(x.is_active))
            for x in self.repo.list_lesson_types()
        ]

    def create_lesson_type(self, body: LessonTypeCreate) -> LessonTypeOut:
        code = body.code.strip()
        if self.repo.get_lesson_type_by_code(code):
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Вид занятий с таким кодом уже есть")
        item = LessonType(code=code, title=body.title.strip(), is_active=1)
        saved = self.repo.save(item)
        return LessonTypeOut(id=saved.id, code=saved.code, title=saved.title, is_active=True)  # type: ignore[attr-defined]

    def update_lesson_type(self, item_id: int, body: LessonTypeUpdate) -> LessonTypeOut:
        item = self.repo.get_lesson_type(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Вид занятий не найден")
        data = body.model_dump(exclude_unset=True)
        if "code" in data and data["code"] is not None:
            code = data["code"].strip()
            other = self.repo.get_lesson_type_by_code(code)
            if other and other.id != item.id:
                raise HTTPException(status.HTTP_409_CONFLICT, detail="Вид занятий с таким кодом уже есть")
            item.code = code
        if "title" in data and data["title"] is not None:
            item.title = data["title"].strip()
        if "is_active" in data and data["is_active"] is not None:
            item.is_active = 1 if data["is_active"] else 0
        saved = self.repo.save(item)
        return LessonTypeOut(
            id=saved.id,  # type: ignore[attr-defined]
            code=saved.code,  # type: ignore[attr-defined]
            title=saved.title,  # type: ignore[attr-defined]
            is_active=_flag(saved.is_active),  # type: ignore[attr-defined]
        )

    def delete_lesson_type(self, item_id: int) -> None:
        item = self.repo.get_lesson_type(item_id)
        if not item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Вид занятий не найден")
        self.repo.delete(item)

    def seed_demo_if_empty(self) -> int:
        counts = self.repo.summary()
        created = 0
        demos: list[object] = []
        if counts["groups"] == 0:
            demos.extend(
                [
                    StudyGroup(code="ИС-21", size=25, education_form="О", specialty_code="09.02.07", study_year=2024),
                    StudyGroup(code="ИС-22", size=24, education_form="О", specialty_code="09.02.07", study_year=2025),
                    StudyGroup(code="ПК-21", size=22, education_form="О", specialty_code="09.02.01", study_year=2024),
                ]
            )
        if counts["teachers"] == 0:
            demos.extend(
                [
                    Teacher(full_name="Иванова Мария Петровна", rate=1.0, budget_flag=1, contacts="ivanova@college.ru"),
                    Teacher(full_name="Сидоров Алексей Николаевич", rate=0.75, budget_flag=1, contacts=None),
                    Teacher(full_name="Козлова Елена Викторовна", rate=1.0, budget_flag=0, contacts="kozlova@college.ru"),
                ]
            )
        if counts["classrooms"] == 0:
            demos.extend(
                [
                    Classroom(code="101", capacity=30, building="А", room_type="лекция"),
                    Classroom(code="215", capacity=16, building="А", room_type="компьютерный"),
                    Classroom(code="304", capacity=28, building="Б", room_type="практика"),
                ]
            )
        if counts["subjects"] == 0:
            demos.extend(
                [
                    Subject(code="ОП.01", title="Операционные системы", short_title="ОС", cycle="ОП"),
                    Subject(code="ОП.02", title="Архитектура аппаратных средств", short_title="Архитектура", cycle="ОП"),
                    Subject(code="МДК.01.01", title="Разработка программных модулей", short_title="РПМ", cycle="ПМ"),
                ]
            )
        if counts.get("specialties", 0) == 0:
            demos.extend(
                [
                    Specialty(code="09.02.07", title="Информационные системы и программирование"),
                    Specialty(code="09.02.01", title="Компьютерные системы и комплексы"),
                    Specialty(code="38.02.01", title="Экономика и бухгалтерский учёт"),
                ]
            )
        if counts.get("lesson_types", 0) == 0:
            demos.extend(
                [
                    LessonType(code="лек", title="Лекция"),
                    LessonType(code="пр", title="Практическое занятие"),
                    LessonType(code="лаб", title="Лабораторная работа"),
                    LessonType(code="конс", title="Консультация"),
                    LessonType(code="экз", title="Экзамен"),
                    LessonType(code="дз", title="Дифференцированный зачёт"),
                ]
            )
        for item in demos:
            self.repo.db.add(item)
            created += 1
        if created:
            self.repo.db.commit()
        return created
