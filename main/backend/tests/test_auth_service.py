"""Unit-тесты AuthService на изолированной in-memory БД."""
import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db import models  # noqa: F401 — register metadata
from app.roles import permissions_for
from app.security import is_bcrypt_hash, verify_password
from app.services.auth import AuthService


@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


def test_seed_creates_three_roles(db):
    service = AuthService(db)
    assert service.seed_default_users() == 3
    assert service.seed_default_users() == 0
    assert service.users.count() == 3
    assert {u.role for u in service.users.list()} == {"admin", "methodist", "dispatcher"}


def test_authenticate_success_creates_session(db):
    service = AuthService(db)
    service.seed_default_users()
    result = service.authenticate("admin", "Admin123!", user_agent="pytest")
    assert result.role == "admin"
    assert result.access_token
    assert result.jti
    assert "users" in result.permissions
    assert service.sessions.is_active(result.jti)


def test_authenticate_wrong_password(db):
    service = AuthService(db)
    service.seed_default_users()
    with pytest.raises(HTTPException) as exc:
        service.authenticate("admin", "bad-pass")
    assert exc.value.status_code == 401


def test_authenticate_unknown_user(db):
    service = AuthService(db)
    with pytest.raises(HTTPException) as exc:
        service.authenticate("nobody", "Admin123!")
    assert exc.value.status_code == 401


def test_create_user_hashes_password_and_validates_role(db):
    service = AuthService(db)
    user = service.create_user(
        login="m2",
        password="Pass123!",
        full_name="Методист 2",
        role="methodist",
    )
    assert is_bcrypt_hash(user.password_hash)
    assert verify_password("Pass123!", user.password_hash)
    assert user.role == "methodist"

    with pytest.raises(HTTPException) as exc:
        service.create_user(login="x", password="Pass123!", full_name="X", role="hacker")
    assert exc.value.status_code == 400


def test_create_user_duplicate(db):
    service = AuthService(db)
    service.create_user(login="dup", password="Pass123!", full_name="A", role="dispatcher")
    with pytest.raises(HTTPException) as exc:
        service.create_user(login="dup", password="Pass123!", full_name="B", role="dispatcher")
    assert exc.value.status_code == 409


def test_logout_revokes_session(db):
    service = AuthService(db)
    service.seed_default_users()
    result = service.authenticate("methodist", "Method123!")
    assert service.sessions.is_active(result.jti)
    assert service.logout(result.jti) is True
    assert service.sessions.is_active(result.jti) is False
    with pytest.raises(HTTPException) as exc:
        service.ensure_active_session(result.jti)
    assert exc.value.status_code == 401


def test_change_password_revokes_sessions(db):
    service = AuthService(db)
    service.seed_default_users()
    result = service.authenticate("dispatcher", "Dispatch123!")
    service.change_password("dispatcher", "Dispatch123!", "Dispatch999!")
    assert service.sessions.is_active(result.jti) is False
    with pytest.raises(HTTPException):
        service.authenticate("dispatcher", "Dispatch123!")
    ok = service.authenticate("dispatcher", "Dispatch999!")
    assert ok.login == "dispatcher"


def test_role_permissions_matrix():
    assert "plans" in permissions_for("methodist")
    assert "schedule" not in permissions_for("methodist")
    assert "schedule" in permissions_for("dispatcher")
    assert "users" in permissions_for("admin")
