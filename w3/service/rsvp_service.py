from model.event import EventStatus
from model.rsvp import RsvpStatus, Rsvp

from service.attendee_service import AttendeeService
from service.event_service import EventService

from repo.rsvp_repo import RsvpRepo
from dto.rsvp_dto import CreateRsvpDto, RsvpDto


class CreateRsvpErrorEventNotFound(Exception):
    pass


class CreateRsvpErrorAttendeeNotFound(Exception):
    pass


class CreateRsvpErrorEventNotOpen(Exception):
    pass


class CreateRsvpErrorAttendeeAlreadyConfirmed(Exception):
    pass


class CreateRsvpErrorAttendeeAlreadyWaitlisted(Exception):
    pass


class RsvpService:
    def __init__(
        self,
        rsvp_repo: RsvpRepo,
        attendee_service: AttendeeService,
        event_service: EventService,
    ) -> None:
        self._repo = rsvp_repo
        self._attendee_service = attendee_service
        self._event_service = event_service

    def create_rsvp(self, request_dto: CreateRsvpDto) -> RsvpDto:
        if not self._event_service.event_exists(request_dto.event_id):
            raise CreateRsvpErrorEventNotFound

        if not self._attendee_service.attendee_exists(request_dto.attendee_id):
            raise CreateRsvpErrorAttendeeNotFound

        target_event = self._event_service.get_event_by_id(request_dto.event_id)
        if not target_event:
            raise CreateRsvpErrorEventNotFound

        if target_event.status != EventStatus.OPEN:
            raise CreateRsvpErrorEventNotOpen

        matching_rsvps = self._repo.get_all_rsvps(
            event_id_filter=request_dto.event_id,
            attendee_id_filter=request_dto.attendee_id,
        )
        if matching_rsvps:
            matching_rsvp = matching_rsvps[0]  # should never be > 1 but anyway
            if matching_rsvp.status == RsvpStatus.CONFIRMED:
                raise CreateRsvpErrorAttendeeAlreadyConfirmed

            if matching_rsvp.status == RsvpStatus.WAITLISTED:
                raise CreateRsvpErrorAttendeeAlreadyWaitlisted

        current_event_capacity = len(
            [
                rsvp
                for rsvp in self._repo.get_all_rsvps(event_id_filter=target_event.id)
                if rsvp.status == RsvpStatus.CONFIRMED
            ]
        )

        if current_event_capacity == target_event.max_capacity:
            created_rsvp = self._repo.create_rsvp(
                request_dto.attendee_id,
                request_dto.event_id,
                RsvpStatus.WAITLISTED,
            )
        else:
            created_rsvp = self._repo.create_rsvp(
                request_dto.attendee_id,
                request_dto.event_id,
                RsvpStatus.CONFIRMED,
            )

        return RsvpDto(
            id=created_rsvp.id,
            attendee_id=created_rsvp.attendee_id,
            event_id=created_rsvp.event_id,
            status=created_rsvp.status,
            created_at=created_rsvp.created_at.isoformat(),
        )

    def get_rsvp_by_id(self, rsvp_id: str) -> RsvpDto | None:
        rsvp: Rsvp | None = self._repo.get_rsvp_by_id(rsvp_id)
        if rsvp is None:
            return None
        return RsvpDto(
            id=rsvp.id,
            attendee_id=rsvp.attendee_id,
            event_id=rsvp.event_id,
            status=rsvp.status,
            created_at=rsvp.created_at.isoformat(),
        )

    def get_all_rsvps(
        self,
        attendee_id_filter: str | None = None,
        event_id_filter: str | None = None,
    ) -> list[RsvpDto]:
        return [
            RsvpDto(
                id=rsvp.id,
                attendee_id=rsvp.attendee_id,
                event_id=rsvp.event_id,
                status=rsvp.status,
                created_at=rsvp.created_at.isoformat(),
            )
            for rsvp in self._repo.get_all_rsvps(
                attendee_id_filter=attendee_id_filter, event_id_filter=event_id_filter
            )
        ]

    def cancel_rsvp(self, rsvp_id: str) -> bool:
        target_rsvp = self._repo.get_rsvp_by_id(rsvp_id)
        if target_rsvp is None:
            return False

        target_rsvp.status = RsvpStatus.CANCELLED

        # get oldest waitlisted reservation for this event
        target_event_id = target_rsvp.event_id
        waitlisted_rsvps = [
            rsvp
            for rsvp in self._repo.get_all_rsvps(event_id_filter=target_event_id)
            if rsvp.status == RsvpStatus.WAITLISTED
        ]
        waitlisted_rsvps = sorted(
            waitlisted_rsvps,
            key=lambda rsvp: rsvp.created_at,
        )

        if waitlisted_rsvps:
            waitlisted_rsvps[0].status = RsvpStatus.CONFIRMED

        return True
