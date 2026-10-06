"""DB engine and session factory."""
from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_settings
from app.db.base import Base

# Import models so metadata is registered before create_all.
from app.db import models  # noqa: F401

_settings = get_settings()
connect_args = {"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {}
engine = create_engine(_settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_engine():
    return engine


def _sqlite_add_column(table: str, column: str, ddl: str) -> None:
    insp = inspect(engine)
    if table not in insp.get_table_names():
        return
    cols = {c["name"] for c in insp.get_columns(table)}
    if column in cols:
        return
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))


def migrate_schema() -> None:
    """Лёгкие ALTER для уже существующей SQLite-БД."""
    if not _settings.database_url.startswith("sqlite"):
        return
    _sqlite_add_column("teachers", "is_active", "is_active INTEGER DEFAULT 1")
    _sqlite_add_column("study_groups", "is_active", "is_active INTEGER DEFAULT 1")
    _sqlite_add_column("classrooms", "is_active", "is_active INTEGER DEFAULT 1")
    _sqlite_add_column("classrooms", "room_type", "room_type VARCHAR(50)")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    migrate_schema()


def get_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
