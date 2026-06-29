import pytest

from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from ...main import app

client = TestClient(app)

def test_home():
    response = client.get("/home")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Async tests

@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        response = await ac.get("/home")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
