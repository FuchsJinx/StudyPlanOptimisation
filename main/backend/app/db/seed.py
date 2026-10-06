"""Database seed helpers."""
from app.db.session import SessionLocal
from app.services.auth import AuthService


def seed_users_if_empty() -> int:
    db = SessionLocal()
    try:
        return AuthService(db).seed_default_users()
    finally:
        db.close()
