"""API tests for public registration."""


def _login(client, login="admin", password="Admin123!"):
    client.post("/api/admin/users/seed")
    res = client.post("/api/auth/login", json={"login": login, "password": password})
    assert res.status_code == 200
    return res.json()


def test_register_creates_user_and_returns_token(client):
    payload = {
        "login": "new.methodist",
        "password": "Secret12",
        "password_confirm": "Secret12",
        "full_name": "Новый Методист",
        "role": "methodist",
        "email": "new@college.ru",
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201, res.text
    body = res.json()
    assert body["login"] == "new.methodist"
    assert body["role"] == "methodist"
    assert "access_token" in body
    assert "plans" in body["permissions"]

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["full_name"] == "Новый Методист"


def test_register_rejects_admin_role(client):
    res = client.post(
        "/api/auth/register",
        json={
            "login": "wanna.admin",
            "password": "Secret12",
            "password_confirm": "Secret12",
            "full_name": "Хакер",
            "role": "admin",
        },
    )
    assert res.status_code == 422


def test_register_password_mismatch(client):
    res = client.post(
        "/api/auth/register",
        json={
            "login": "mismatch.user",
            "password": "Secret12",
            "password_confirm": "Secret99",
            "full_name": "Несовпадение",
            "role": "dispatcher",
        },
    )
    assert res.status_code == 400
    assert "совпадают" in res.json()["detail"].lower() or "совпад" in res.json()["detail"].lower()


def test_register_duplicate_login(client):
    _login(client)
    res = client.post(
        "/api/auth/register",
        json={
            "login": "methodist",
            "password": "Secret12",
            "password_confirm": "Secret12",
            "full_name": "Дубликат",
            "role": "methodist",
        },
    )
    assert res.status_code == 409
