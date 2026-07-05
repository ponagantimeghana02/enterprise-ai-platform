from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_upload_document_success(tmp_path):
    response = client.post(
        "/documents/upload",
        files={"file": ("sample.pdf", b"%PDF-1.4\n%test", "application/pdf")},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "Document uploaded successfully."
    assert body["filename"].endswith(".pdf")
    assert body["storage_path"].endswith(".pdf")


def test_upload_document_duplicate_rejected():
    first = client.post(
        "/documents/upload",
        files={"file": ("duplicate.txt", b"hello world", "text/plain")},
    )
    second = client.post(
        "/documents/upload",
        files={"file": ("duplicate.txt", b"hello world", "text/plain")},
    )

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "Duplicate document detected."
