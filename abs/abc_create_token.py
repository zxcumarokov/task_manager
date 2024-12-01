from abc import ABC, abstractmethod
from datetime import datetime


class ICreateToken(ABC):
    @abstractmethod
    def create_token(
        self,
        username: str,
        expire_date_time: datetime,  # expire_time = datetime.utcnow() + timedelta(hours=1) через 1 час
    ) -> str:
        raise NotImplementedError
