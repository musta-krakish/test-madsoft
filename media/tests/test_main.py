import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_upload_file():
    file_content = b"this is a test file"
    files = {"file": ("test_file.jpg", file_content, "image/jpeg")}

    response = await client.post("/upload/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "filename" in data
    assert data["filename"] == "test_file.jpg"
