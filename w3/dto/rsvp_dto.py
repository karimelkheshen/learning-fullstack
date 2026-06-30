from dataclasses import dataclass


@dataclass(frozen=True)
class CreateRsvpDto:
    attendee_id: str
    event_id: str


@dataclass(frozen=True)
class RsvpDto:
    id: str
    attendee_id: str
    event_id: str
    status: str
    created_at: str
