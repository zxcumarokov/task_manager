import os
from datetime import datetime

import asyncpg
import jwt
from dotenv import load_dotenv

from abs.abc_token_storage import ITockenStorage
from models.user import User


class TokenStorage(ITockenStorage):
    def __init__(self, database_url: str):
        """Инициализирует хранилище с клиентом базы данных."""
        self.database_url = database_url
        if not self.database_url:
            raise ValueError("DATABASE_URL не указан в .env файле")

    async def _connect(self):
        """Создает асинхронное подключение к базе данных."""
        return await asyncpg.connect(self.database_url)

    async def create_token(self, username: str, expire_date_time: datetime) -> str:
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

        load_dotenv()
        SECRET_KEY = os.getenv("SECRET_KEY")
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY не указан в .env файле")

        # Генерация токена
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token

    async def save_tokens(self, user: User) -> None:
        """Сохраняет токены пользователя в базу данных."""
        conn = await self._connect()
        try:
            query = """
                UPDATE users
                SET encrypted_refresh_token = $1,
                    encrypted_access_token = $2
                WHERE username = $3
            """
            await conn.execute(
                query,
                user.encrypted_refresh_token,
                user.encrypted_access_token,
                user.username,
            )
        finally:
            await conn.close()
