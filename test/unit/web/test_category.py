from fastapi.testclient import TestClient
import os
import importlib

def _setup_client(tmp_path):
    # point the app/data to a temporary sqlite file for isolation
    db_file = tmp_path / "test_personal_finances.db"
    os.environ["PERFIN_SQLITE_DB"] = str(db_file)

    # reload modules that create DB connections at import time
    import data.init as data_init
    importlib.reload(data_init)

    import main as app_module
    importlib.reload(app_module)

    return TestClient(app_module.app)

def test_get_categories_empty(tmp_path):
    client = _setup_client(tmp_path)
    resp = client.get("/api/categories")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_create_and_list_category(tmp_path):
    client = _setup_client(tmp_path)
    payload = {"name": "TestCategory", "description": "Test description"}
    resp = client.post("/api/categories", json=payload)
    assert resp.status_code in (200, 201)
    created = resp.json()
    assert created["name"] == payload["name"]
    assert created["description"] == payload["description"]

    resp = client.get("/api/categories")
    assert resp.status_code == 200
    items = resp.json()
    assert any(item.get("name") == payload["name"] for item in items)