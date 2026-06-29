from fastapi.testclient import TestClient

from ...main import app
from ...routers.dependency import common_parameters

client = TestClient(app)

def test_read_items_with_dependencies_valid_header():
    response = client.get("/dependency/items/dependencies", headers={"X-Token": "fake-super-secret-token", "X-key": "fake-super-secret-key"})
    assert response.status_code == 200

def test_read_items_with_dependencies_invalid_header():
    response = client.get("/dependency/items/dependencies", headers={"X-Token": "wrong-token", "X-key": "wrong-key"})
    assert response.status_code == 400

# Override dependency

async def override_dependency(q: str | None = None):
    return {"q": q, "skip": 5, "limit": 10}

app.dependency_overrides[common_parameters] = override_dependency

def test_read_items_with_dependency():
    response = client.get("/dependency/items/")
    assert response.status_code == 200
    assert response.json() == {"q": None, "skip": 5, "limit": 10}

# You can reset your overrides (remove them) by setting app.dependency_overrides to be an empty dict
# app.dependency_overrides = {}
