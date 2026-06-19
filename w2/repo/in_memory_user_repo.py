from repo.user_repo import UserRepo
from model.user import User


class InMemoryUserRepo(UserRepo):
    def __init__(self) -> None:
        super().__init__()
        self._users = {}

    def create_user(self, data: dict) -> User:
        """
        creates a user and adds them to the repo
        """
        user = User(**data)
        self._users[user.id] = user
        return user

    def get_user_by_id(self, user_id: str) -> User | None:
        """
        returns the user if found, otherwise null
        """
        return self._users.get(user_id, None)
