from abc import ABC, abstractmethod
from datetime import datetime


class ICreateToken(ABC):
    @abstractmethod
    def create_token(
        self,
        username: str,
        expire_date_time: datetime,
    ) -> str:
        raise NotImplementedError
