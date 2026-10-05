"""Journal / OCR reconciliation models."""
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JournalDocument(Base):
    __tablename__ = "journal_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    period: Mapped[str | None] = mapped_column(String(50), nullable=True)
    uploaded_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("journal_documents.id"), nullable=False)
    teacher_id: Mapped[int | None] = mapped_column(ForeignKey("teachers.id"), nullable=True)
    discipline_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hours_fact: Mapped[float | None] = mapped_column(Float, nullable=True)
    hours_plan: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    deviation_flag: Mapped[str | None] = mapped_column(String(20), nullable=True)
