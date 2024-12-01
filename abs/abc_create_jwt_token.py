from abc import ABC, abstractmethod


class ICreateJwtToken(ABC):
    @abstractmethod
    def create_token(self, secret_key: str, refresh_token: str) -> str:
        raise NotImplementedError
