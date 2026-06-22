from model.attendee import Attendee
from dto.attendee_dto import CreateAttendeeRequestDto, AttendeeDto
from repo.attendee_repo import AttendeeRepo


class AttendeeService:
    def __init__(self, attendee_repo: AttendeeRepo) -> None:
        self._attendee_repo = attendee_repo

    def create_attendee(self, request_dto: CreateAttendeeRequestDto) -> AttendeeDto:
        created_attendee: Attendee = self._attendee_repo.add_attendee(
            name=request_dto.name,
            email=request_dto.email,
        )
        return AttendeeDto(
            id=created_attendee.id,
            name=created_attendee.name,
            email=created_attendee.email,
            created_at=created_attendee.created_at,
        )

    def get_all_attendees(self) -> list[AttendeeDto]:
        return [
            AttendeeDto(
                id=attendee.id,
                name=attendee.name,
                email=attendee.email,
                created_at=attendee.created_at,
            )
            for attendee in self._attendee_repo.get_all_attendees()
        ]

    def get_attendee_by_id(self, attendee_id: str) -> AttendeeDto | None:
        found_attendee = self._attendee_repo.get_attendee_by_id(attendee_id)
        if found_attendee is None:
            return None
        return AttendeeDto(
            id=found_attendee.id,
            name=found_attendee.name,
            email=found_attendee.email,
            created_at=found_attendee.created_at,
        )

    def delete_attendee(self, attendee_id: str) -> bool:
        return self._attendee_repo.delete_attendee(attendee_id)
