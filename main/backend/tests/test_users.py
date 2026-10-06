"""Users database and auth tests."""
from fastapi.testclient import TestClient

from app.db.session import SessionLocal, init_db
from app.main import create_app
from app.repositories.users import UserRepository
from app.services.auth import AuthService


def _fresh_client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_users.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file.as_posix()}")
    # reset settings cache and engine would be complex; use dedicated app init_db on same URL
    from app.config import get_settings

    get_settings.cache_clear()
    # Re-create engine bindings for test is heavy; test against running models via service + API lifespan
    app = create_app()
    return TestClient(app), db_file


def test_seed_creates_three_default_users():
    init_db()
    db = SessionLocal()
    try:
        # wipe users for isolated assertion when possible
        for u in UserRepository(db).list(limit=1000):
            db.delete(u)
        db.commit()

        created = AuthService(db).seed_default_users()
        assert created == 3
        assert UserRepository(db).count() == 3

        created_again = AuthService(db).seed_default_users()
        assert created_again == 0
    finally:
        db.close()


def test_login_success_and_fail(client: TestClient):
    # ensure seed
    client.post("/api/admin/users/seed")

    ok = client.post("/api/auth/login", json={"login": "admin", "password": "Admin123!"})
    assert ok.status_code == 200
    data = ok.json()
    assert data["role"] == "admin"
    assert data["access_token"]

    bad = client.post("/api/auth/login", json={"login": "admin", "password": "wrong"})
    assert bad.status_code == 401


def test_create_user_via_admin(client: TestClient):
    client.post("/api/admin/users/seed")
    res = client.post(
        "/api/admin/users",
        json={
            "login": "teacher1",
            "password": "Teach123!",
            "full_name": "Преподаватель Тест",
            "role": "methodist",
            "email": "t1@local",
        },
    )
    # may 201 or 409 if rerun
    assert res.status_code in (201, 409)
    users = client.get("/api/admin/users")
    assert users.status_code == 200
    assert any(u["login"] == "admin" for u in users.json())
