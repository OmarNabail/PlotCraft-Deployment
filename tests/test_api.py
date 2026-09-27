from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_generate_endpoint():
    response = client.post(
        "/generate",
        json={"prompt": "Create a bar chart"},
    )

    assert response.status_code == 200
    assert "matplotlib" in response.json()["generated_code"]


def test_generate_endpoint_rejects_blank_prompt():
    response = client.post("/generate", json={"prompt": "   "})

    assert response.status_code == 400
