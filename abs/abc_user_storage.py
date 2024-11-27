from abc import ABC, abstractmethod

from models import User


class IUserStorage(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> User:
        raise NotImplementedError
