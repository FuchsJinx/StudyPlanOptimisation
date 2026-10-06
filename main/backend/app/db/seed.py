"""Database seed helpers."""
from app.db.session import SessionLocal
from app.services.auth import AuthService
from app.services.refs import RefsService


def seed_users_if_empty() -> int:
    db = SessionLocal()
    try:
        return AuthService(db).seed_default_users()
    finally:
        db.close()


def seed_directories_if_empty() -> int:
    db = SessionLocal()
    try:
        return RefsService(db).seed_demo_if_empty()
    finally:
        db.close()
