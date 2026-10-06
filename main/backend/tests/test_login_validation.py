"""Login request validation tests."""


def test_login_rejects_empty_password(client):
    res = client.post("/api/auth/login", json={"login": "admin", "password": ""})
    assert res.status_code == 422


def test_login_rejects_bad_login_chars(client):
    res = client.post("/api/auth/login", json={"login": "админ", "password": "Admin123!"})
    assert res.status_code == 422


def test_login_wrong_password_is_401(client):
    client.post("/api/admin/users/seed")
    res = client.post("/api/auth/login", json={"login": "admin", "password": "wrong!"})
    assert res.status_code == 401


def test_login_ok_after_seed(client):
    client.post("/api/admin/users/seed")
    res = client.post("/api/auth/login", json={"login": "admin", "password": "Admin123!"})
    assert res.status_code == 200
    assert res.json()["role"] == "admin"
