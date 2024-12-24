from abc import ABC, abstractmethod


class ITokenVerifier(ABC):
    @abstractmethod
    def verify_token(self, token: str) -> str:
        """
        Проверяет валидность токена, расшифровывает и декодирует его.

        :param token: Зашифрованный токен.
        :return: Идентификатор пользователя, извлечённый из токена.
        :raises HTTPException: Если токен невалиден или истёк.
        """
        raise NotImplementedError
