"""ORM models."""
from app.db.models.user import User
from app.db.models.refs import Classroom, StudyGroup, Teacher
from app.db.models.curriculum import CurriculumPlan, PlanDiscipline
from app.db.models.workload import WorkloadAssignment
from app.db.models.schedule import ScheduleSlot, Substitution
from app.db.models.journal import JournalDocument, JournalEntry

__all__ = [
    "User",
    "Teacher",
    "StudyGroup",
    "Classroom",
    "CurriculumPlan",
    "PlanDiscipline",
    "WorkloadAssignment",
    "ScheduleSlot",
    "Substitution",
    "JournalDocument",
    "JournalEntry",
]
