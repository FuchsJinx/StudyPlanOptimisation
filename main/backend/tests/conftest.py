"""Pytest fixtures."""
import pytest
from fastapi.testclient import TestClient

from app.db.session import SessionLocal, init_db
from app.main import create_app
from app.services.auth import AuthService, DEFAULT_USERS
from app.security import hash_password


def _reset_default_users() -> None:
    """Гарантирует наличие дефолтных пользователей с исходными паролями."""
    init_db()
    db = SessionLocal()
    try:
        from app.db.models.session import UserSession
        from app.db.models.user import User

        db.query(UserSession).delete()
        for item in DEFAULT_USERS:
            user = db.query(User).filter(User.login == item["login"]).one_or_none()
            if user is None:
                user = User(
                    login=item["login"],
                    password_hash=hash_password(item["password"]),
                    full_name=item["full_name"],
                    role=item["role"],
                    email=item["email"],
                    is_active=True,
                )
                db.add(user)
            else:
                user.password_hash = hash_password(item["password"])
                user.is_active = True
                user.role = item["role"]
                db.add(user)
        db.commit()
    finally:
        db.close()


@pytest.fixture()
def client():
    _reset_default_users()
    app = create_app()
    with TestClient(app) as c:
        yield c
