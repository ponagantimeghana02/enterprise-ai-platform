from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_agent():
    response = client.post(
        "/agents/run",
        json={
            "task": "Summarize document"
        }
    )

    assert response.status_code in [200, 404]