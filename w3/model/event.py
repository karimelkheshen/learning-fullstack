from uuid import uuid4
from enum import Enum
from datetime import datetime, timezone
from dataclasses import dataclass, field


class EventStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


@dataclass
class Event:
    title: str
    description: str
    start_time: datetime
    max_capacity: int
    status: EventStatus
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
