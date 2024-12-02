from abc import ABC, abstractmethod

from models import User


class IUserStorage(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def save_tokens(self, user: User) -> None:
        raise NotImplementedError
