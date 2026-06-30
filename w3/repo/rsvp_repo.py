from model.rsvp import Rsvp, RsvpStatus


class RsvpRepo:
    def __init__(self) -> None:
        self._repo = {}

    def create_rsvp(self, attendee_id: str, event_id: str, status: RsvpStatus) -> Rsvp:
        rsvp = Rsvp(attendee_id=attendee_id, event_id=event_id, status=status)
        self._repo[rsvp.id] = rsvp
        return rsvp

    def get_rsvp_by_id(self, rsvp_id: str) -> Rsvp | None:
        return self._repo.get(rsvp_id, None)

    def get_all_rsvps(
        self, event_id_filter: str | None = None, attendee_id_filter: str | None = None
    ):
        results: list[Rsvp] = list(self._repo.values())
        if event_id_filter:
            results = [rsvp for rsvp in results if rsvp.event_id == event_id_filter]
        if attendee_id_filter:
            results = [
                rsvp for rsvp in results if rsvp.attendee_id == attendee_id_filter
            ]
        return results

    def cancel_rsvp(self, rsvp_id: str) -> Rsvp | None:
        rsvp: Rsvp | None = self._repo.get(rsvp_id, None)
        if rsvp is None:
            return None
        rsvp.status = RsvpStatus.CANCELLED
        self._repo[rsvp.id] = rsvp
        return rsvp
