from abc import ABC, abstractmethod

from models.user import User


class ITokenStorage(ABC):
    @abstractmethod
    async def save_tokens(self, user: User) -> None:
        """Сохраняет токены (refresh и access) в базу данных."""
        raise NotImplementedError
