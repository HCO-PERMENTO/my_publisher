import json
from fastapi.testclient import TestClient
from server import app, DATA_FILE

client = TestClient(app)


def setup_function():
    if DATA_FILE.exists():
        DATA_FILE.unlink()
    DATA_FILE.write_text("[]", encoding="utf-8")


def test_save_and_get_idea():
    payload = {
        "title": "Test idé",
        "subtitle": "Sub",
        "bullets": ["A", "B"],
        "raw_idea": "rå",
        "conversation": ["hej", "hvordan"],
        "status": "ny",
    }

    resp = client.post("/save_idea", json=payload)
    assert resp.status_code == 200
    idea_id = resp.json()["id"]

    get_resp = client.get(f"/get_idea/{idea_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["title"] == "Test idé"


def test_update_and_delete_idea():
    resp = client.post("/save_idea", json={"title": "X", "status": "ny"})
    idea_id = resp.json()["id"]

    upd = client.put(f"/update_idea/{idea_id}", json={"status": "klar"})
    assert upd.status_code == 200
    assert upd.json()["status"] == "klar"

    del_resp = client.delete(f"/delete_idea/{idea_id}")
    assert del_resp.status_code == 200

    missing = client.get(f"/get_idea/{idea_id}")
    assert missing.status_code == 404
