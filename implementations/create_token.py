import os
from datetime import datetime

import jwt
from dotenv import load_dotenv

from abs.abc_create_token import ICreateToken

# Загрузка секретного ключа
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не указан в .env файле")


class CreateToken(ICreateToken):
    def create_token(
        self,
        username: str,
        expire_date_time: datetime,
    ) -> str:
        """
        Создает токен для пользователя.
        :param username: Имя пользователя
        :param expire_date_time: Время истечения токена
        :return: Строка токена
        """
        payload = {
            "username": username,  # Имя пользователя
            "exp": expire_date_time,  # Время истечения токена
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")  # Подпись токена
        return token
