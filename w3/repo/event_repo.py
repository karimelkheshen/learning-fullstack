from math import ceil
from datetime import datetime
from enum import Enum

from model.event import Event, EventStatus


class EventsRepo:
    PAGINATION_PER_PAGE_MIN: int = 10
    PAGINATION_PER_PAGE_MAX: int = 100

    def __init__(self):
        self._events = {}

    def create_event(
        self,
        title: str,
        description: str,
        start_time: datetime,
        max_capacity: int,
        status: EventStatus,
    ) -> Event:
        event = Event(
            title=title,
            description=description,
            start_time=start_time,
            max_capacity=max_capacity,
            status=status,
        )
        self._events[event.id] = event
        return event

    def get_event_by_id(self, event_id: str):
        return self._events.get(event_id, None)

    def get_all_events(
        self,
        status_filter: EventStatus | None = None,
        sort_by_start_time_asc: bool | None = None,
        page: int | None = 1,
        per_page: int | None = PAGINATION_PER_PAGE_MIN,
    ) -> tuple[int, int, list[Event]]:
        results = list(self._events.values())

        if status_filter:
            results = [event for event in results if event.status == status_filter]

        if sort_by_start_time_asc is not None:
            sorted(
                results,
                key=lambda item: item.start_time,
                reverse=not sort_by_start_time_asc,
            )

        if page is None:
            page = 1
        if per_page is None:
            per_page = self.PAGINATION_PER_PAGE_MIN

        if per_page < self.PAGINATION_PER_PAGE_MIN:
            per_page = self.PAGINATION_PER_PAGE_MIN
        if per_page > self.PAGINATION_PER_PAGE_MAX:
            per_page = self.PAGINATION_PER_PAGE_MAX

        total_items = len(results)
        max_page = ceil(total_items / per_page) if total_items > 0 else 1

        if page < 1:
            page = 1
        if page > max_page:
            page = max_page

        offset = (page - 1) * per_page

        return page, per_page, results[offset : offset + per_page]

    def update_event(
        self,
        event_id: str,
        title: str,
        description: str,
        start_time: datetime,
        max_capacity: int,
        status: EventStatus,
    ) -> Event | None:
        target_event = self._events.get(event_id, None)

        if target_event is None:
            return None

        new_event = Event(
            id=event_id,
            title=title,
            description=description,
            start_time=start_time,
            max_capacity=max_capacity,
            status=status,
            created_at=target_event.created_at,
        )

        self._events[event_id] = new_event

        return new_event

    def delete_event(self, event_id: str) -> bool:
        event_found = self._events.get(event_id, None)
        if event_found is None:
            return False
        del self._events[event_id]
        return True
