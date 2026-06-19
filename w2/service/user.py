from pydantic import ValidationError

from repo.user_repo import UserRepo
from model.user import User


class InvalidUserFieldsError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self._repo = user_repo

    def add_user(self, data: dict) -> User:
        try:
            user = self._repo.create_user(data)
            return user
        except TypeError:
            raise InvalidRequestError
        except ValidationError:
            raise InvalidUserFieldsError

    def get_user_by_id(self, user_id: str) -> User | None:
        return self._repo.get_user_by_id(user_id)
