def test_add_user_valid(client):
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
    created_user = response.get_json()["details"]
    assert created_user["username"] == test_username
    assert created_user["email"] == test_email
    assert created_user["id"] is not None
    assert created_user["created_at"] is not None


def test_add_user_invalid_request(client):
    test_email = "karim@gmail.com"
    response = client.post(
        "/users",
        json={
            "email": test_email,
        },
    )

    assert response.status_code == 400


def test_add_user_invalid_username(client):
    invalid_username = "kar"
    valid_email = "karim@gmail.com"
    response = client.post(
        "/users",
        json={
            "username": invalid_username,
            "email": valid_email,
        },
    )

    assert response.status_code == 400


def test_add_user_invalid_email(client):
    valid_username = "karimelkheshen"
    invalid_email = "karim@gmail"
    response = client.post(
        "/users",
        json={
            "username": valid_username,
            "email": invalid_email,
        },
    )

    assert response.status_code == 400


def test_get_user_by_id_not_found(client):
    response = client.get("/users/unknown")
    assert response.status_code == 404


def test_get_user_by_id_found(client, created_user):
    user_id = created_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
