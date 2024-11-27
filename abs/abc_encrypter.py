from abc import ABC, abstractmethod


class IEncrypter(ABC):
    @abstractmethod
    def encrypt(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, encrypted_password: str) -> str:
        raise NotImplementedError
