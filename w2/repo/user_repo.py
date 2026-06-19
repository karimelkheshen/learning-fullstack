from abc import ABC, abstractmethod

from model.user import User


class UserRepo(ABC):
    @abstractmethod
    def create_user(self, data: dict) -> User: ...

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None: ...
