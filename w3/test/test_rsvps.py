from datetime import datetime, timedelta


def test_create_rsvp_request_invalid(client, created_event):
    invalid_payload = {"invalid_key": "invalid_value"}
    res = client.post(f"/events/{created_event['id']}/rsvps", json=invalid_payload)
    assert res.status_code == 400


def test_create_rsvp_request_invalid_attendee_not_found(client, created_event):
    payload = {"attendee_id": "unknown"}
    res = client.post(f"/events/{created_event['id']}/rsvps", json=payload)
    assert res.status_code == 404


def test_create_rsvp_request_invalid_event_not_found(client, created_attendee):
    payload = {"attendee_id": created_attendee["id"]}
    res = client.post("/events/unknown/rsvps", json=payload)
    assert res.status_code == 404


def test_create_rsvp_request_invalid_event_not_open(
    client,
    created_event_not_open,
    created_attendee,
):
    payload = {"attendee_id": created_attendee["id"]}
    res = client.post(f"/events/{created_event_not_open['id']}/rsvps", json=payload)
    assert res.status_code == 409


def test_create_rsvp_request_invalid_event_attendee_already_confirmed(
    client,
    created_attendee,
    created_event,
):
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendee["id"]},
    )

    assert res.status_code == 201

    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendee["id"]},
    )

    assert res.status_code == 409


def test_create_rsvp_request_invalid_event_attendee_already_waitlisted(
    client,
    created_attendees,
):
    # create a max capacity 1 event
    res = client.post(
        "/events",
        json={
            "title": "test",
            "description": "test",
            "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "max_capacity": 1,
            "status": "open",
        },
    )
    assert res.status_code == 201
    created_event = res.get_json()["data"]

    # attendee 1 confirmed
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendees[0]["id"]},
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["status"] == "confirmed"

    # attendee 2 waitlisted
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendees[1]["id"]},
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["status"] == "waitlisted"

    # attendee 2 re-attempts reservation: should fail with 409
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendees[1]["id"]},
    )

    assert res.status_code == 409


def test_create_rsvp_request_valid_attendee_confirmed(
    client,
    created_event,
    created_attendee,
):
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendee["id"]},
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["status"] == "confirmed"


def test_create_rsvp_request_valid_attendee_waitlisted(client, created_attendees):
    # create a max capacity 1 event
    res = client.post(
        "/events",
        json={
            "title": "test",
            "description": "test",
            "start_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "max_capacity": 1,
            "status": "open",
        },
    )
    assert res.status_code == 201
    created_event = res.get_json()["data"]

    # attendee 1 confirmed
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendees[0]["id"]},
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["status"] == "confirmed"

    # attendee 2 waitlisted
    res = client.post(
        f"events/{created_event['id']}/rsvps",
        json={"attendee_id": created_attendees[1]["id"]},
    )
    assert res.status_code == 201
    assert res.get_json()["data"]["status"] == "waitlisted"


def test_get_rsvp_by_id_not_found(client):
    res = client.get(f"/rsvps/unknown")
    assert res.status_code == 404


def test_get_rsvp_by_id(client, created_rsvp):
    res = client.get(f"/rsvps/{created_rsvp['id']}")
    assert res.status_code == 200
    assert res.get_json()["data"]["id"] == created_rsvp["id"]


def test_cancel_rsvp_request_invalid_rsvp_not_found(client):
    res = client.delete("/rsvps/unknown")
    assert res.status_code == 404


def test_cancel_rsvp_request_valid(client, created_rsvp):
    res = client.delete(f"/rsvps/{created_rsvp['id']}")
    assert res.status_code == 204
    res = client.get(f"/rsvps/{created_rsvp['id']}")
    assert res.status_code == 200
    assert res.get_json()["data"]["status"] == "cancelled"


def test_get_all_rsvps_event_not_found(client):
    res = client.get("/events/unknown/rsvps")
    assert res.status_code == 404


def test_get_all_rsvps_request_valid_empty(client, created_event):
    res = client.get(f"/events/{created_event['id']}/rsvps")
    assert res.status_code == 200
    assert res.get_json()["data"] == []


def test_get_all_rsvps_request_valid(client, created_rsvp):
    res = client.get(f"/events/{created_rsvp['event_id']}/rsvps")
    assert res.status_code == 200
    expected_rsvp_ids = [created_rsvp["id"]]
    received_rsvp_ids = [rsvp["id"] for rsvp in res.get_json()["data"]]
    assert expected_rsvp_ids == received_rsvp_ids
