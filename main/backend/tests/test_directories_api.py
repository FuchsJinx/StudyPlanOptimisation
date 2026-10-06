"""API tests for directories and role access."""


def _login(client, login="admin", password="Admin123!"):
    client.post("/api/admin/users/seed")
    res = client.post("/api/auth/login", json={"login": login, "password": password})
    assert res.status_code == 200
    return res.json()


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_directories_in_permissions(client):
    data = _login(client, "dispatcher", "Dispatch123!")
    assert "directories" in data["permissions"]
    assert "plans" not in data["permissions"]


def test_summary_requires_auth(client):
    assert client.get("/api/directories/summary").status_code == 401


def test_dispatcher_can_read_but_not_write(client):
    data = _login(client, "dispatcher", "Dispatch123!")
    headers = _auth(data["access_token"])
    assert client.get("/api/directories/groups", headers=headers).status_code == 200
    denied = client.post(
        "/api/directories/groups",
        headers=headers,
        json={"code": "X-99", "education_form": "О"},
    )
    assert denied.status_code == 403


def test_methodist_crud_group(client):
    data = _login(client, "methodist", "Method123!")
    headers = _auth(data["access_token"])
    created = client.post(
        "/api/directories/groups",
        headers=headers,
        json={
            "code": "TEST-01",
            "size": 20,
            "education_form": "О",
            "specialty_code": "09.02.07",
            "study_year": 2026,
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["code"] == "TEST-01"
    item_id = body["id"]

    listed = client.get("/api/directories/groups", headers=headers)
    assert listed.status_code == 200
    assert any(g["id"] == item_id for g in listed.json())

    patched = client.patch(
        f"/api/directories/groups/{item_id}",
        headers=headers,
        json={"size": 21},
    )
    assert patched.status_code == 200
    assert patched.json()["size"] == 21

    deleted = client.delete(f"/api/directories/groups/{item_id}", headers=headers)
    assert deleted.status_code == 204


def test_seed_summary_counts(client):
    data = _login(client, "admin", "Admin123!")
    headers = _auth(data["access_token"])
    # seed runs on app startup; ensure at least empty summary works
    summary = client.get("/api/directories/summary", headers=headers)
    assert summary.status_code == 200
    body = summary.json()
    assert {"groups", "teachers", "classrooms", "subjects"}.issubset(body.keys())


def test_subjects_and_teachers_create(client):
    data = _login(client, "admin", "Admin123!")
    headers = _auth(data["access_token"])
    t = client.post(
        "/api/directories/teachers",
        headers=headers,
        json={"full_name": "Test Teacher Unique", "rate": 1.0, "budget_flag": True},
    )
    assert t.status_code == 201
    s = client.post(
        "/api/directories/subjects",
        headers=headers,
        json={"code": "TST-UNIQ-01", "title": "Test subject unique", "cycle": "OP"},
    )
    assert s.status_code == 201, s.text
    c = client.post(
        "/api/directories/classrooms",
        headers=headers,
        json={"code": "ROOM-UNIQ-999", "capacity": 10, "building": "T", "room_type": "lab"},
    )
    assert c.status_code == 201, c.text
