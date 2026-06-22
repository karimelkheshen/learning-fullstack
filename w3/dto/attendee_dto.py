from datetime import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAttendeeRequestDto:
    name: str
    email: str


@dataclass(frozen=True)
class AttendeeDto:
    id: str
    name: str
    email: str
    created_at: datetime
