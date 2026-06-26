from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

def test_read_item_with_http_exception_existing_item():
    response = client.get("/error/items/foo")
    assert response.status_code == 200
    assert response.json() == {"item": {"name": "Foo", "price": 50.2}}

def test_read_item_with_http_exception_missing_item():
    response = client.get("/error/items/dom")
    assert response.status_code == 404
