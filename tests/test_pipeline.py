from fastapi.testclient import TestClient
from worker import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_job():
    r = client.post("/jobs", json={"episode":"content/demo_episode.json"})
    assert r.status_code == 200
    assert r.json()["status"] == "accepted"
