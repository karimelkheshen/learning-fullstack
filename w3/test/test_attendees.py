import pytest


def test_create_attendee_valid(client):
    payload = {"name": "test", "email": "test@test.com"}
    response = client.post("/attendees", json=payload)
    assert response.status_code == 201
    created_attendee = response.get_json()["data"]
    assert "created_at" in created_attendee.keys()
    assert "id" in created_attendee.keys()


@pytest.mark.parametrize(
    "field, invalid_value",
    [
        ("name", ""),
        ("email", "invalid_email"),
    ],
)
def test_create_attendee_invalid_fields(client, field, invalid_value):
    payload = {"name": "test", "email": "test@test.com"}
    payload[field] = invalid_value
    response = client.post("/attendees", json=payload)
    assert response.status_code == 400


def test_get_all_attendees_empty(client):
    response = client.get("/attendees")
    assert response.status_code == 200
    attendee_list = response.get_json()["data"]
    assert attendee_list == []


def test_get_all_attendees(client, created_attendees):
    expected_attendee_ids = [attendee["id"] for attendee in created_attendees]
    response = client.get("/attendees")
    assert response.status_code == 200
    attendee_list = response.get_json()["data"]
    assert expected_attendee_ids == [attendee["id"] for attendee in attendee_list]


def test_get_attendee_by_id_found(client, created_attendee):
    expected_id = created_attendee["id"]
    response = client.get(f"/attendees/{expected_id}")
    assert response.status_code == 200
    assert response.get_json()["data"]["id"] == expected_id


def test_get_attendee_by_id_not_found(client):
    response = client.get("/attendees/unknown")
    assert response.status_code == 404


def test_delete_attendee_found(client, created_attendee):
    target_id = created_attendee["id"]
    response = client.delete(f"/attendees/{target_id}")
    assert response.status_code == 204


def test_delete_attendee_not_found(client):
    response = client.delete(f"/attendees/unknown")
    assert response.status_code == 404
