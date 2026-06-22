from dataclasses import dataclass

from service.attendee_service import AttendeeService


@dataclass
class ServiceContainer:
    attendee_service: AttendeeService
