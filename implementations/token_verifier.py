# implementations/TokenVerifier.py

import jwt
from fastapi import HTTPException

from abs import ITokenVerifier  # Импортируем ITokenVerifier
from implementations.encrypter import FernetEncrypter


class TokenVerifier(ITokenVerifier):
    def __init__(self, secret_key: str, encrypter: FernetEncrypter):
        """
        Инициализация TokenVerifier.
        :param secret_key: Секретный ключ для подписи JWT токенов.
        :param encrypter: Шифратор для зашифровки/расшифровки токенов.
        """
        self.secret_key = secret_key
        self.encrypter = encrypter

    def verify_token(self, token: str) -> str:
        """
        Проверяет и расшифровывает токен JWT.
        :param token: Зашифрованный JWT токен.
        :return: user_id из токена.
        :raises HTTPException: Если токен истек, имеет неверный формат или не может быть расшифрован.
        """
        # Попытка расшифровать токен
        try:
            decrypted_token = self.encrypter.decrypt(token)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail="Invalid token format or decryption error"
            )

        # Попытка декодировать JWT токен
        try:
            decoded_token = jwt.decode(
                decrypted_token, self.secret_key, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Token expired. Please refresh your token."
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=400, detail="Invalid token. Please check the token."
            )

        # Проверка на наличие нужных данных в токене
        if "user_id" not in decoded_token:
            raise HTTPException(
                status_code=400, detail="Token does not contain user_id"
            )

        return decoded_token["user_id"]
