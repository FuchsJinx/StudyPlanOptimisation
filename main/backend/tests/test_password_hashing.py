"""Unit-тесты хеширования паролей (bcrypt)."""
from app.db.models.user import User
from app.db.session import SessionLocal, init_db
from app.security import hash_password, is_bcrypt_hash, verify_password
from app.services.auth import AuthService


def test_hash_is_bcrypt_and_not_plaintext():
    plain = "Secret123!"
    hashed = hash_password(plain)
    assert hashed != plain
    assert is_bcrypt_hash(hashed)
    assert plain not in hashed


def test_verify_accepts_correct_password():
    plain = "Secret123!"
    hashed = hash_password(plain)
    assert verify_password(plain, hashed) is True
    assert verify_password("other", hashed) is False


def test_same_password_different_salts():
    plain = "SamePass1!"
    h1 = hash_password(plain)
    h2 = hash_password(plain)
    assert h1 != h2
    assert verify_password(plain, h1)
    assert verify_password(plain, h2)


def test_rejects_plaintext_stored_as_hash():
    assert verify_password("Admin123!", "Admin123!") is False


def test_create_user_stores_only_hash():
    init_db()
    db = SessionLocal()
    try:
        service = AuthService(db)
        # cleanup if exists
        existing = service.users.get_by_login("hash_demo")
        if existing:
            db.delete(existing)
            db.commit()
        user = service.create_user(
            login="hash_demo",
            password="DemoPass1!",
            full_name="Hash Demo",
            role="methodist",
        )
        assert user.password_hash != "DemoPass1!"
        assert is_bcrypt_hash(user.password_hash)
        assert verify_password("DemoPass1!", user.password_hash)
    finally:
        demo = db.query(User).filter(User.login == "hash_demo").one_or_none()
        if demo:
            db.delete(demo)
            db.commit()
        db.close()


def test_change_password_rehashes(client):
    client.post("/api/admin/users/seed")
    login = client.post("/api/auth/login", json={"login": "methodist", "password": "Method123!"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    changed = client.post(
        "/api/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"current_password": "Method123!", "new_password": "Method999!"},
    )
    assert changed.status_code == 200

    old = client.post("/api/auth/login", json={"login": "methodist", "password": "Method123!"})
    assert old.status_code == 401
    new = client.post("/api/auth/login", json={"login": "methodist", "password": "Method999!"})
    assert new.status_code == 200

    # restore default for other tests
    token2 = new.json()["access_token"]
    client.post(
        "/api/auth/change-password",
        headers={"Authorization": f"Bearer {token2}"},
        json={"current_password": "Method999!", "new_password": "Method123!"},
    )
