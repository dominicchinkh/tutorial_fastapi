from fastapi.testclient import TestClient

from ..main import app, ml_models

client = TestClient(app)

def test_read_items():
    # Before the lifespan starts, "items" is still empty
    assert ml_models == {}

    with TestClient(app) as client:
        # Inside the "with TestClient" block, the lifespan starts and items added
        assert ml_models == {'answer_to_everything': 'fake_answer_to_everything_ml_model'}

    # The end of the "with TestClient" block simulates terminating the app, so
    # the lifespan ends and items are cleaned up
    assert ml_models == {}
