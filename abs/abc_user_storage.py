from abc import ABC, abstractmethod

from models import User


class IUserStorage(ABC):
    @abstractmethod
    async def get_user(self, username: str) -> User:
        """Получает пользователя по имени."""
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> None:
        """Создаёт нового пользователя."""
        raise NotImplementedError

    @abstractmethod
    async def save_tokens(self, user: User) -> None:
        """Обновляет токены пользователя."""
        raise NotImplementedError

    @abstractmethod
    async def update_tokens(
        self, username: str, encrypted_access_token: str, encrypted_refresh_token: str
    ) -> None:
        """Обновляет токены пользователя в базе данных."""
        raise NotImplementedError
