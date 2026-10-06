"""Reference directories API with role-based access."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.deps import get_db, require_permission, require_roles
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
from app.services.refs import RefsService

router = APIRouter()

# Просмотр справочников — все роли с правом directories
CanView = Depends(require_permission("directories"))
# Изменение — методист и администратор
CanEdit = Depends(require_roles("admin", "methodist"))


@router.get("/summary", response_model=DirectorySummary)
def summary(db: Session = Depends(get_db), _: User = CanView) -> DirectorySummary:
    return RefsService(db).summary()


# ---- groups ----
@router.get("/groups", response_model=list[StudyGroupOut])
def list_groups(db: Session = Depends(get_db), _: User = CanView) -> list[StudyGroupOut]:
    return RefsService(db).list_groups()


@router.post("/groups", response_model=StudyGroupOut, status_code=201)
def create_group(
    body: StudyGroupCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> StudyGroupOut:
    return RefsService(db).create_group(body)


@router.patch("/groups/{item_id}", response_model=StudyGroupOut)
def update_group(
    item_id: int,
    body: StudyGroupUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> StudyGroupOut:
    return RefsService(db).update_group(item_id, body)


@router.delete("/groups/{item_id}", status_code=204)
def delete_group(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_group(item_id)


# ---- teachers ----
@router.get("/teachers", response_model=list[TeacherOut])
def list_teachers(db: Session = Depends(get_db), _: User = CanView) -> list[TeacherOut]:
    return RefsService(db).list_teachers()


@router.post("/teachers", response_model=TeacherOut, status_code=201)
def create_teacher(
    body: TeacherCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> TeacherOut:
    return RefsService(db).create_teacher(body)


@router.patch("/teachers/{item_id}", response_model=TeacherOut)
def update_teacher(
    item_id: int,
    body: TeacherUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> TeacherOut:
    return RefsService(db).update_teacher(item_id, body)


@router.delete("/teachers/{item_id}", status_code=204)
def delete_teacher(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_teacher(item_id)


# ---- classrooms ----
@router.get("/classrooms", response_model=list[ClassroomOut])
def list_classrooms(db: Session = Depends(get_db), _: User = CanView) -> list[ClassroomOut]:
    return RefsService(db).list_classrooms()


@router.post("/classrooms", response_model=ClassroomOut, status_code=201)
def create_classroom(
    body: ClassroomCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> ClassroomOut:
    return RefsService(db).create_classroom(body)


@router.patch("/classrooms/{item_id}", response_model=ClassroomOut)
def update_classroom(
    item_id: int,
    body: ClassroomUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> ClassroomOut:
    return RefsService(db).update_classroom(item_id, body)


@router.delete("/classrooms/{item_id}", status_code=204)
def delete_classroom(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_classroom(item_id)


# ---- subjects ----
@router.get("/subjects", response_model=list[SubjectOut])
def list_subjects(db: Session = Depends(get_db), _: User = CanView) -> list[SubjectOut]:
    return RefsService(db).list_subjects()


@router.post("/subjects", response_model=SubjectOut, status_code=201)
def create_subject(
    body: SubjectCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> SubjectOut:
    return RefsService(db).create_subject(body)


@router.patch("/subjects/{item_id}", response_model=SubjectOut)
def update_subject(
    item_id: int,
    body: SubjectUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> SubjectOut:
    return RefsService(db).update_subject(item_id, body)


@router.delete("/subjects/{item_id}", status_code=204)
def delete_subject(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_subject(item_id)


# ---- specialties ----
@router.get("/specialties", response_model=list[SpecialtyOut])
def list_specialties(db: Session = Depends(get_db), _: User = CanView) -> list[SpecialtyOut]:
    return RefsService(db).list_specialties()


@router.post("/specialties", response_model=SpecialtyOut, status_code=201)
def create_specialty(
    body: SpecialtyCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> SpecialtyOut:
    return RefsService(db).create_specialty(body)


@router.patch("/specialties/{item_id}", response_model=SpecialtyOut)
def update_specialty(
    item_id: int,
    body: SpecialtyUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> SpecialtyOut:
    return RefsService(db).update_specialty(item_id, body)


@router.delete("/specialties/{item_id}", status_code=204)
def delete_specialty(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_specialty(item_id)


# ---- lesson types ----
@router.get("/lesson-types", response_model=list[LessonTypeOut])
def list_lesson_types(db: Session = Depends(get_db), _: User = CanView) -> list[LessonTypeOut]:
    return RefsService(db).list_lesson_types()


@router.post("/lesson-types", response_model=LessonTypeOut, status_code=201)
def create_lesson_type(
    body: LessonTypeCreate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> LessonTypeOut:
    return RefsService(db).create_lesson_type(body)


@router.patch("/lesson-types/{item_id}", response_model=LessonTypeOut)
def update_lesson_type(
    item_id: int,
    body: LessonTypeUpdate,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> LessonTypeOut:
    return RefsService(db).update_lesson_type(item_id, body)


@router.delete("/lesson-types/{item_id}", status_code=204)
def delete_lesson_type(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = CanEdit,
) -> None:
    RefsService(db).delete_lesson_type(item_id)
