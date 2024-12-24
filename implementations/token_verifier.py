import logging
from datetime import datetime

import jwt
from fastapi import HTTPException

from abs import ITokenVerifier
from implementations.encrypter import FernetEncrypter

logger = logging.getLogger(__name__)


class TokenVerifier(ITokenVerifier):
    def __init__(self, secret_key: str, encrypter: FernetEncrypter):
        """
        Инициализация класса для проверки токенов.
        :param secret_key: Секретный ключ для декодирования JWT.
        :param encrypter: Экземпляр шифровальщика для расшифровки токенов.
        """
        self.secret_key = secret_key
        self.encrypter = encrypter

    def verify_token(self, token: str) -> str:
        """
        Проверяет и валидирует токен.
        :param token: Зашифрованный токен.
        :return: Идентификатор пользователя из токена.
        :raises HTTPException: Если токен невалиден или истёк.
        """
        try:
            logger.debug(f"Verifying token: {token}")
            decrypted_token = self.encrypter.decrypt(token)
            logger.debug(f"Decrypted token: {decrypted_token}")

            # Декодирование токена с отключенной проверкой срока действия
            decoded_token = jwt.decode(
                decrypted_token,
                self.secret_key,
                algorithms=["HS256"],
                options={"verify_exp": False},
            )
            user_id = decoded_token.get("user_id")
            exp = decoded_token.get("exp")
            logger.debug(f"Decoded token: {decoded_token}")

            if not user_id:
                raise HTTPException(
                    status_code=401, detail="User ID not found in token"
                )

            # Проверка на истечение срока действия токена
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=401, detail="Token expired. Please refresh your token."
                )

            return user_id

        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            raise HTTPException(
                status_code=401, detail="Token expired. Please refresh your token."
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"JWT error: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError as e:
            logger.error(f"Decryption or token parsing failed: {str(e)}")
            raise HTTPException(
                status_code=400, detail="Invalid token format or decryption error"
            )
