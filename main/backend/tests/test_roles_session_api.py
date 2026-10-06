"""API tests for roles, logout and session."""


def _login(client, login="admin", password="Admin123!"):
    client.post("/api/admin/users/seed")
    res = client.post("/api/auth/login", json={"login": login, "password": password})
    assert res.status_code == 200
    return res.json()


def test_login_returns_permissions(client):
    data = _login(client, "methodist", "Method123!")
    assert "plans" in data["permissions"]
    assert "users" not in data["permissions"]


def test_admin_users_requires_admin_role(client):
    meth = _login(client, "methodist", "Method123!")
    denied = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {meth['access_token']}"},
    )
    assert denied.status_code == 403

    adm = _login(client, "admin", "Admin123!")
    ok = client.get(
        "/api/admin/users",
        headers={"Authorization": f"Bearer {adm['access_token']}"},
    )
    assert ok.status_code == 200


def test_logout_invalidates_token(client):
    data = _login(client)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    assert client.get("/api/auth/me", headers=headers).status_code == 200
    assert client.post("/api/auth/logout", headers=headers).status_code == 200
    assert client.get("/api/auth/me", headers=headers).status_code == 401


def test_session_endpoint(client):
    data = _login(client, "dispatcher", "Dispatch123!")
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    res = client.get("/api/auth/session", headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["role"] == "dispatcher"
    assert body["is_authenticated"] is True
    assert "substitutions" in body["permissions"]


def test_roles_catalog(client):
    res = client.get("/api/auth/roles")
    assert res.status_code == 200
    ids = {r["id"] for r in res.json()["roles"]}
    assert ids == {"admin", "methodist", "dispatcher"}
