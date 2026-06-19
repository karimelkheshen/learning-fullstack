from dataclasses import dataclass
from service.user import UserService
from service.task import TaskService


@dataclass
class ServicesContainer:
    user_service: UserService
    task_service: TaskService
