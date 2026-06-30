from model.event import Event
from repo.event_repo import EventsRepo
from dto.event_dto import (
    CreateEventRequestDto,
    EventDto,
    UpdateEventRequestDto,
    GetAllEventsRequestDto,
    GetAllEventsResponseDto,
)


class EventService:
    def __init__(self, events_repo: EventsRepo) -> None:
        self._repo = events_repo

    def create_event(self, request_dto: CreateEventRequestDto) -> EventDto:

        new_event = self._repo.create_event(
            request_dto.title,
            request_dto.description,
            request_dto.start_time,
            request_dto.max_capacity,
            request_dto.status,
        )

        return EventDto(
            title=new_event.title,
            description=new_event.description,
            start_time=new_event.start_time.isoformat(),
            max_capacity=new_event.max_capacity,
            status=new_event.status,
            id=new_event.id,
            created_at=new_event.created_at.isoformat(),
        )

    def event_exists(self, event_id: str) -> bool:
        found_event = self._repo.get_event_by_id(event_id)
        return found_event is not None

    def get_event_by_id(self, event_id: str) -> EventDto | None:
        event_found = self._repo.get_event_by_id(event_id)
        if event_found is None:
            return None
        return EventDto(
            title=event_found.title,
            description=event_found.description,
            start_time=event_found.start_time,
            max_capacity=event_found.max_capacity,
            status=event_found.status,
            id=event_found.id,
            created_at=event_found.created_at,
        )

    def get_all_events(
        self, request_dto: GetAllEventsRequestDto
    ) -> GetAllEventsResponseDto:
        page, per_page, results = self._repo.get_all_events(
            status_filter=request_dto.status_filter,
            sort_by_start_time_asc=request_dto.sort_by_start_time_asc,
            page=request_dto.page,
            per_page=request_dto.per_page,
        )

        results = [
            EventDto(
                title=event.title,
                description=event.description,
                start_time=event.start_time.isoformat(),
                max_capacity=event.max_capacity,
                status=event.status,
                id=event.id,
                created_at=event.created_at.isoformat(),
            )
            for event in results
        ]

        return GetAllEventsResponseDto(page=page, per_page=per_page, results=results)

    def update_event(
        self, event_id: str, request_dto: UpdateEventRequestDto
    ) -> EventDto | None:

        updated_event = self._repo.update_event(
            event_id=event_id,
            title=request_dto.title,
            description=request_dto.description,
            start_time=request_dto.start_time,
            max_capacity=request_dto.max_capacity,
            status=request_dto.status,
        )

        if updated_event is None:
            return None

        return EventDto(
            title=updated_event.title,
            description=updated_event.description,
            start_time=updated_event.start_time.isoformat(),
            max_capacity=updated_event.max_capacity,
            status=updated_event.status,
            id=updated_event.id,
            created_at=updated_event.created_at.isoformat(),
        )

    def delete_event(self, event_id: str) -> bool:
        return self._repo.delete_event(event_id)
