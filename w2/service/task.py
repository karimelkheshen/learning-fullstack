from pydantic import ValidationError

from model.task import Task, TaskPriority, TaskStatus
from repo.task_repo import TaskRepo
from service.user import UserService


class TaskNotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class InvalidTaskFieldsError(Exception):
    pass


class TaskService:
    def __init__(
        self,
        task_repo: TaskRepo,
        user_service: UserService,
    ) -> None:
        self._task_repo = task_repo
        self._user_service = user_service

    def add_task(self, data: dict) -> Task:
        """
        adds a new task to the repo
        raises InvalidRequestError on invalid request format
        raises UserNotFoundException if user with owner_id not found.
        raises InvalidTaskFieldsError on invalid fields
        """
        # make sure owner_id exists in users repo
        owner_id = data.get("owner_id", None)
        if not owner_id:
            raise InvalidRequestError
        user = self._user_service.get_user_by_id(owner_id)
        if user is None:
            raise UserNotFoundException

        try:
            task = self._task_repo.add_task(data)
            return task
        except TypeError:
            raise InvalidRequestError
        except ValidationError:
            raise InvalidTaskFieldsError

    def get_task_by_id(self, task_id: str) -> Task:
        """
        returns task if found
        raises TaskNotFoundException if not found
        """
        task = self._task_repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundException
        return task

    def get_all_tasks(
        self,
        priority_filter: TaskPriority | None,
        status_filter: TaskStatus | None,
    ) -> list[Task]:
        """
        returns all tasks with optional priority filter
        raises InvalidRequestError on invalid request
        """
        try:
            tasks = self._task_repo.get_all_tasks(
                priority_filter,
                status_filter,
            )
            return tasks
        except TypeError:
            raise InvalidRequestError

    def update_task(self, task_id: str, data: dict) -> Task:
        """
        updates a task and returns it
        raises InvalidRequestError on invalid request format
        raises TaskNotFoundException if task not found
        raises InvalidTaskFieldsError on invalid fields
        """
        try:
            updated_task = self._task_repo.update_task(task_id, data)
            if updated_task is None:
                raise TaskNotFoundException
            return updated_task
        except TypeError:
            raise InvalidRequestError
        except ValidationError:
            raise InvalidTaskFieldsError

    def delete_task(self, task_id: str) -> bool:
        """returns the task was deleted or not"""
        return self._task_repo.delete_task(task_id)
