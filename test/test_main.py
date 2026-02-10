from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_app_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
