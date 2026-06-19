from abc import ABC, abstractmethod

from model.task import Task, TaskStatus, TaskPriority


class TaskRepo(ABC):
    @abstractmethod
    def add_task(self, data: dict) -> Task: ...

    @abstractmethod
    def get_task_by_id(self, task_id: str) -> Task | None: ...

    @abstractmethod
    def get_all_tasks(
        self,
        priority_filter: TaskPriority | None = None,
        status_filter: TaskStatus | None = None,
    ) -> list[Task]: ...

    @abstractmethod
    def update_task(self, task_id: str, data: dict) -> Task | None: ...

    @abstractmethod
    def delete_task(self, task_id: str) -> bool: ...
