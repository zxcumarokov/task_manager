from abc import ABC, abstractmethod
from datetime import datetime

from models.user import User


class ITockenStorage(ABC):
    @abstractmethod
    async def create_access_token(
        self,
        username: str,
        expire_date_time: datetime,  # expire_time = datetime.utcnow() + timedelta(hours=1) через 1 час
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(
        self,
        username: str,
    ) -> str:
        """
        Создает refresh токен с более длительным временем жизни (например, через несколько дней).
        :param username: Имя пользователя
        :return: Строка refresh токена
        """
        raise NotImplementedError

    @abstractmethod
    async def save_tokens(self, user: User) -> None:
        raise NotImplementedError
