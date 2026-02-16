from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_recipe():
    response = client.post(
        "/api/v1/recipes/",
        json={
            "title": "Тестовый рецепт",
            "ingredients": ["яйцо"],
            "steps": ["разбить яйцо"],
            "tags": ["тест"],
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовый рецепт"
    assert "id" in data


def test_get_recipes():
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_recipe():
    response = client.get("/api/v1/recipes/9999")
    assert response.status_code == 404
