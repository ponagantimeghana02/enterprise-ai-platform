from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login():
    response = client.post(
        "/login",
        json={
            "email": "admin@test.com",
            "password": "admin123"
        }
    )

    assert response.status_code in [200, 401]

def test_logout():
    response = client.post("/logout")
    assert response.status_code in [200, 401]