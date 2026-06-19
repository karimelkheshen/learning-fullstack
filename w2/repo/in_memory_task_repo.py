from repo.task_repo import TaskRepo

from model.task import Task, TaskStatus, TaskPriority


class InMemoryTaskRepo(TaskRepo):

    def __init__(self) -> None:
        super().__init__()
        self._tasks = {}

    def add_task(self, data: dict) -> Task:
        """
        adds a new task to the repo and returns it on success
        raises a pydantic validation error if creation failed
        """
        task = Task(**data)
        self._tasks[task.id] = task
        return task

    def get_task_by_id(self, task_id: str) -> Task | None:
        """returns task if found, none otherwise"""
        return self._tasks.get(task_id, None)

    def get_all_tasks(
        self,
        priority_filter: TaskPriority | None = None,
        status_filter: TaskStatus | None = None,
    ) -> list[Task]:
        """returns all tasks with optional priority filter applied"""
        results = list(self._tasks.values())
        if priority_filter:
            results = [task for task in results if task.priority == priority_filter]
        if status_filter:
            results = [task for task in results if task.status == status_filter]
        return results

    def update_task(self, task_id: str, data: dict) -> Task | None:
        """
        updates the target task and returns it on success or none if task_id not found.
        raises a pydantic validation error if creation failed
        """
        target_task: Task | None = self._tasks.get(task_id, None)
        if not target_task:
            return None

        new_task = Task(
            id=task_id,
            title=data.get("title", target_task.title),
            description=data.get("description", target_task.description),
            status=data.get("status", target_task.status),
            priority=data.get("priority", target_task.priority),
            owner_id=target_task.owner_id,
            created_at=target_task.created_at,
        )

        self._tasks[task_id] = new_task
        return new_task

    def delete_task(self, task_id: str) -> bool:
        if task_id not in self._tasks.keys():
            return False
        del self._tasks[task_id]
        return True
