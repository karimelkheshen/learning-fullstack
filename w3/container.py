from dataclasses import dataclass

from service.attendee_service import AttendeeService
from service.event_service import EventService


@dataclass
class ServiceContainer:
    attendee_service: AttendeeService
    event_service: EventService
