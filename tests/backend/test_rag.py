from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_rag_search():
    response = client.post(
        "/rag/search",
        json={
            "query": "Leave Policy"
        }
    )

    assert response.status_code in [200, 404]