from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

def test_read_items_with_dependencies_valid_header():
    response = client.get("/dependency/items/dependencies", headers={"X-Token": "fake-super-secret-token", "X-key": "fake-super-secret-key"})
    assert response.status_code == 200

def test_read_items_with_dependencies_invalid_header():
    response = client.get("/dependency/items/dependencies", headers={"X-Token": "wrong-token", "X-key": "wrong-key"})
    assert response.status_code == 400
