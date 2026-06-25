from datetime import datetime
from dataclasses import dataclass

from model.event import EventStatus


@dataclass(frozen=True)
class CreateEventRequestDto:
    title: str
    description: str
    start_time: datetime
    max_capacity: int
    status: EventStatus


@dataclass(frozen=True)
class UpdateEventRequestDto:
    title: str
    description: str
    start_time: datetime
    max_capacity: int
    status: EventStatus


@dataclass(frozen=True)
class GetAllEventsRequestDto:
    status_filter: EventStatus | None
    sort_by_start_time_asc: bool | None
    page: int | None
    per_page: int | None


@dataclass(frozen=True)
class EventDto:
    title: str
    description: str
    start_time: str
    max_capacity: int
    status: EventStatus
    id: str
    created_at: str


@dataclass(frozen=True)
class GetAllEventsResponseDto:
    page: int
    per_page: int
    results: list[EventDto]
