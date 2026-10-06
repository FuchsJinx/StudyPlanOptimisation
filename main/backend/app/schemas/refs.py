"""Pydantic schemas for reference directories."""
from pydantic import BaseModel, ConfigDict, Field


class DirectorySummary(BaseModel):
    groups: int
    teachers: int
    classrooms: int
    subjects: int
    specialties: int = 0
    lesson_types: int = 0


class StudyGroupCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    size: int | None = Field(default=None, ge=1, le=500)
    education_form: str = Field(default="О", max_length=5)
    specialty_code: str | None = Field(default=None, max_length=30)
    study_year: int | None = Field(default=None, ge=2000, le=2100)


class StudyGroupUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    size: int | None = Field(default=None, ge=1, le=500)
    education_form: str | None = Field(default=None, max_length=5)
    specialty_code: str | None = Field(default=None, max_length=30)
    study_year: int | None = Field(default=None, ge=2000, le=2100)
    is_active: bool | None = None


class StudyGroupOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    size: int | None = None
    education_form: str
    specialty_code: str | None = None
    study_year: int | None = None
    is_active: bool


class TeacherCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    rate: float | None = Field(default=None, ge=0, le=2)
    budget_flag: bool = True
    contacts: str | None = Field(default=None, max_length=255)


class TeacherUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    rate: float | None = Field(default=None, ge=0, le=2)
    budget_flag: bool | None = None
    contacts: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class TeacherOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    rate: float | None = None
    budget_flag: bool
    contacts: str | None = None
    is_active: bool


class ClassroomCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    capacity: int | None = Field(default=None, ge=1, le=500)
    building: str | None = Field(default=None, max_length=50)
    room_type: str | None = Field(default=None, max_length=50)


class ClassroomUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    capacity: int | None = Field(default=None, ge=1, le=500)
    building: str | None = Field(default=None, max_length=50)
    room_type: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class ClassroomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    capacity: int | None = None
    building: str | None = None
    room_type: str | None = None
    is_active: bool


class SubjectCreate(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    title: str = Field(min_length=2, max_length=255)
    short_title: str | None = Field(default=None, max_length=80)
    cycle: str | None = Field(default=None, max_length=20)


class SubjectUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    title: str | None = Field(default=None, min_length=2, max_length=255)
    short_title: str | None = Field(default=None, max_length=80)
    cycle: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class SubjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    short_title: str | None = None
    cycle: str | None = None
    is_active: bool



class SpecialtyCreate(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    title: str = Field(min_length=2, max_length=255)


class SpecialtyUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=30)
    title: str | None = Field(default=None, min_length=2, max_length=255)
    is_active: bool | None = None


class SpecialtyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    title: str
    is_active: bool


class LessonTypeCreate(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    title: str = Field(min_length=2, max_length=120)


class LessonTypeUpdate(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=30)
    title: str | None = Field(default=None, min_length=2, max_length=120)
    is_active: bool | None = None


class LessonTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    code: str
    title: str
    is_active: bool
