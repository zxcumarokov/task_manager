import logging
import os

import asyncpg
from dotenv import load_dotenv

from abs.abc_task_storage import ITaskStorage
from models import Task

logging.basicConfig(level=logging.DEBUG)


class TaskStorage(ITaskStorage):
    def __init__(self):
        load_dotenv()  # Загрузка переменных из .env
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL не указан в .env файле")

    async def _connect(self):
        """Создает асинхронное подключение к базе данных."""
        return await asyncpg.connect(self.database_url)

    async def create_task(self, task: Task) -> int:
        """Создает задачу в базе данных и возвращает ее ID."""
        conn = await self._connect()
        try:
            # Выполняем вставку и получаем ID
            query = """
                INSERT INTO tasks (title, description, status)
                VALUES ($1, $2, $3)
                RETURNING id
            """
            task_id = await conn.fetchval(
                query, task.title, task.description, task.status
            )
            return task_id
        finally:
            await conn.close()

    async def upgrade_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ) -> None:
        """Обновляет задачу в базе данных. Поля title, description и status необязательны."""
        if not (title or description or status):
            raise ValueError("Нужно передать хотя бы одно поле для обновления.")

        # Формируем динамическую часть запроса
        updates = []

        values: list[
            str | int
        ] = []  # Используйте str | int, если список содержит оба типа

        # Добавляем параметры только если они не None
        if title is not None:
            updates.append("title = ${}".format(len(values) + 1))  # Следующий индекс
            values.append(title)
        if description is not None:
            updates.append(
                "description = ${}".format(len(values) + 1)
            )  # Следующий индекс
            values.append(description)
        if status is not None:
            updates.append("status = ${}".format(len(values) + 1))  # Следующий индекс
            values.append(status)

        # Добавляем ID задачи в конец списка значений
        values.append(int(task_id))

        # Формируем запрос
        query = f"""
        UPDATE tasks
        SET {", ".join(updates)}
        WHERE id = ${len(values)}  -- Последний индекс будет ID
        """

        conn = await self._connect()
        try:
            logging.debug(f"Executing query: {query} with values: {values}")
            # Выполняем запрос с параметрами
            await conn.execute(query, *values)
            logging.debug("Task updated successfully.")
        except Exception as e:
            logging.error(f"Error while updating task: {e}")
            raise Exception(f"An error occurred while updating task: {e}")
        finally:
            await conn.close()

    async def delete_task(self, task_id: int) -> None:
        """Удаляет задачу из базы данных по ID."""
        conn = await self._connect()
        try:
            query = """
            DELETE FROM tasks
            WHERE id = $1
            """
            await conn.execute(query, task_id)
        finally:
            await conn.close()

    async def get_task_by_id(self, task_id: int) -> Task:
        """Получает задачу из базы данных по ID."""
        conn = await self._connect()
        try:
            query = """
            SELECT id, title, description, status
            FROM tasks
            WHERE id = $1
            """
            row = await conn.fetchrow(query, task_id)
            if not row:
                raise ValueError(f"Задача с ID {task_id} не найдена.")
            return Task(**row)  # Преобразуем данные в объект Task
        finally:
            await conn.close()
