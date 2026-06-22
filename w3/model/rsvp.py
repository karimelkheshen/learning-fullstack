from uuid import uuid4
from datetime import datetime, timezone
from enum import Enum
from dataclasses import dataclass, field


class RsvpStatus(str, Enum):
    CONFIRMED = "confirmed"
    WAITLISTED = "waitlisted"
    CANCELLED = "cancelled"


@dataclass
class Rsvp:
    attendee_id: str
    event_id: str
    status: RsvpStatus
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
