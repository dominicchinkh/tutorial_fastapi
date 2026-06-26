from fastapi.testclient import TestClient

from ...main import app

client = TestClient(app)

def test_create_hero_valid_json():
    response = client.post(
        "/database/heroes",
        json={
            "name": "dominic",
            "age": 18,
            "secret_name": "the-secret-word"
        },
    )
    assert response.status_code == 200
    r = response.json()
    assert r["name"] == "dominic" and r["age"] == 18

def test_create_hero_invalid_json():
    response = client.post(
        "/database/heroes",
        json={
            "venue": "bangkok",
            "food": "tom-yam"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": [
                    "body",
                    "name"
                ],
                "msg": "Field required",
                "input": {
                    "venue": "bangkok",
                    "food": "tom-yam"
                }
            },
            {
                "type": "missing",
                "loc": [
                    "body",
                    "secret_name"
                ],
                "msg": "Field required",
                "input": {
                    "venue": "bangkok",
                    "food": "tom-yam"
                }
            }
        ]
    }
