import logging
import os
from abc import ABC, abstractmethod
from typing import List, Optional

import asyncpg
import jwt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from abs import ITaskStorage
from implementations.encrypter import FernetEncrypter
from models import Task

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TaskStorage(ITaskStorage):
    def __init__(self, encrypter: FernetEncrypter):
        self.encrypter = encrypter
        load_dotenv()  # Загрузка переменных из .env
        self.database_url = os.getenv("DATABASE_URL")
        self.secret_key = os.getenv("SECRET_KEY")  # Секретный ключ для JWT токенов
        if not self.database_url:
            raise ValueError("DATABASE_URL не указан в .env файле")
        if not self.secret_key:
            raise ValueError("SECRET_KEY не указан в .env файле")

    async def _connect(self):
        """Создает асинхронное подключение к базе данных."""
        return await asyncpg.connect(self.database_url)

    def _verify_token(self, token: str) -> int:
        """Проверка и декодирование токена."""
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = decoded_token.get("user_id")
            if not user_id:
                raise ValueError("User ID not found in token")
            return user_id
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.JWTError as e:
            raise ValueError("Invalid token")

    async def create_task(self, task: Task, token: str) -> int:
        logger.debug(f"Creating task: {task.title}")
        user_id = self._verify_token(token)
        conn = await self._connect()
        try:
            query = """
                INSERT INTO tasks (title, description, status, user_id)
                VALUES ($1, $2, $3, $4)
                RETURNING id
            """
            task_id = await conn.fetchval(
                query, task.title, task.description, task.status, user_id
            )
            logger.debug(f"Task inserted with ID: {task_id}")
            return task_id
        finally:
            await conn.close()

    async def upgrade_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        logger.debug(f"Updating task with ID: {task_id}")
        conn = await self._connect()
        try:
            query = """
                UPDATE tasks
                SET title = COALESCE($1, title),
                    description = COALESCE($2, description),
                    status = COALESCE($3, status)
                WHERE id = $4
            """
            await conn.execute(query, title, description, status, task_id)
            logger.debug(f"Task with ID: {task_id} updated successfully.")
        finally:
            await conn.close()

    async def delete_task(self, task_id: int) -> None:
        logger.debug(f"Deleting task with ID: {task_id}")
        conn = await self._connect()
        try:
            query = "DELETE FROM tasks WHERE id = $1"
            await conn.execute(query, task_id)
            logger.debug(f"Task with ID: {task_id} deleted successfully.")
        finally:
            await conn.close()

    async def get_task_by_id(self, task_id: int) -> Task:
        logger.debug(f"Getting task with ID: {task_id}")
        conn = await self._connect()
        try:
            query = "SELECT * FROM tasks WHERE id = $1"
            row = await conn.fetchrow(query, task_id)
            if row:
                task = Task(**dict(row))
                logger.debug(f"Task retrieved: {task}")
                return task
            else:
                raise ValueError(f"Task with ID {task_id} not found.")
        finally:
            await conn.close()

    async def get_tasks_by_user_id(self, user_id: int) -> List[Task]:
        logger.debug(f"Getting tasks for user ID: {user_id}")
        conn = await self._connect()
        try:
            query = "SELECT * FROM tasks WHERE user_id = $1"
            rows = await conn.fetch(query, user_id)
            tasks = [Task(**dict(row)) for row in rows]
            logger.debug(f"Retrieved {len(tasks)} tasks for user {user_id}.")
            return tasks
        finally:
            await conn.close()
