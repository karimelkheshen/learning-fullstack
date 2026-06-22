import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def created_user(client):
    test_username = "karimelkheshen"
    test_email = "karim@gmail.com"
    response = client.post(
        "/users",
        json={
            "username": test_username,
            "email": test_email,
        },
    )
    assert response.status_code == 201
    return response.get_json()["details"]
