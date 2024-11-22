import os

import psycopg
from dotenv import load_dotenv

from abs.abc_task_storage import ITaskStorage
from models import Task


class TaskStorage(ITaskStorage):
    def __init__(self):
        load_dotenv()  # Загрузка переменных из .env
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL не указан в .env файле")

        # Проверяем, если формат URI, преобразуем в параметры
        if self.database_url.startswith("postgres://"):
            self.database_url = self._convert_uri_to_params(self.database_url)

    @staticmethod
    def _convert_uri_to_params(uri: str) -> str:
        """Конвертирует строку подключения из формата URI в строку параметров."""
        from psycopg.conninfo import conninfo_to_dict, make_conninfo

        conninfo = make_conninfo(uri)
        params_dict = conninfo_to_dict(conninfo)
        return " ".join(f"{key}={value}" for key, value in params_dict.items())

    def create_task(self, task: Task) -> int:
        """Создает задачу в базе данных и возвращает ее ID."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, description, status)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (task.title, task.description, task.status),
                )
                # Получаем только ID новой записи
                task_id = cursor.fetchone()[0]
                conn.commit()
                return task_id

    def upgrade_task(
        self,
        task_id: int,
        title: str,
        description: str,
        status: str,
    ) -> None:
        """Обновляет задачу в базе данных. Поля title, description и status необязательны."""
        if not (title or description or status):
            raise ValueError("Нужно передать хотя бы одно поле для обновления.")

        # Формируем динамическую часть запроса
        updates = []
        values = []
        if title:
            updates.append("title = %s")
            values.append(title)
        if description:
            updates.append("description = %s")
            values.append(description)
        if status:
            updates.append("status = %s")
            values.append(status)

        # Добавляем ID задачи в конец списка значений
        values.append(task_id)

        query = f"""
        UPDATE tasks
        SET {", ".join(updates)}
        WHERE id = %s
        """

        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()

    def delete_task(self, task_id: int) -> None:
        """Удаляет задачу из базы данных по ID."""
        with psycopg.connect(self.database_url) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,),
                )
                conn.commit()

    def get_task_by_id(self, task_id: int) -> Task:
        """Получает задачу из базы данных по ID."""
        with psycopg.connect(self.database_url, row_factory=class_row(Task)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, description, status
                    FROM tasks
                    WHERE id = %s
                    """,
                    (task_id,),
                )
                task = cursor.fetchone()
                if not task:
                    raise ValueError(f"Задача с ID {task_id} не найдена.")
                return task
