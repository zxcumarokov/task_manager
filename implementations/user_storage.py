import os

import asyncpg
from dotenv import load_dotenv

from abs.abc_user_storage import IUserStorage  # Ваш интерфейс
from models import User  # Ваш объект User


class UserStorage(IUserStorage):
    def __init__(self):
        load_dotenv()  # Загрузка переменных из .env
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL не указан в .env файле")

    async def _connect(self):
        """Создает асинхронное подключение к базе данных."""
        return await asyncpg.connect(self.database_url)

    async def create_user(self, user: User) -> None:
        """Добавляет нового пользователя в базу данных."""
        conn = await self._connect()
        try:
            query = """
            INSERT INTO users (username, encrypted_password, encrypted_refresh_token, encrypted_access_token)
            VALUES ($1, $2, $3, $4)
            """
            await conn.execute(
                query,
                user.username,
                user.encrypted_password,
                user.encrypted_refresh_token,
                user.encrypted_access_token,
            )
        finally:
            await conn.close()

    async def get_user(self, username: str) -> User:
        """Получает пользователя из базы данных по имени."""
        conn = await self._connect()
        try:
            query = """
            SELECT username, encrypted_password, encrypted_refresh_token, encrypted_access_token
            FROM users
            WHERE username = $1
            """
            row = await conn.fetchrow(query, username)
            if not row:
                raise ValueError(f"Пользователь с именем {username} не найден.")
            return User(
                username=row["username"],
                encrypted_password=row["encrypted_password"],
                encrypted_refresh_token=row["encrypted_refresh_token"],
                encrypted_access_token=row["encrypted_access_token"],
            )
        finally:
            await conn.close()

    async def save_tokens(self, user: User) -> None:
        """Обновляет токены пользователя в базе данных."""
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
