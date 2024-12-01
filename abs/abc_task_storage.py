from abc import ABC, abstractmethod

from models import Task


class ITaskStorage(ABC):
    @abstractmethod
    async def create_task(self, task: Task) -> int:
        """
        Создает новую задачу и возвращает её ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def upgrade_task(
        self,
        task_id: int,
        title: str | None,
        description: str | None,
        status: str | None,
    ) -> None:
        """
        Обновляет задачу в базе данных.
        Можно передать одно или несколько полей (title, description, status).
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу из базы данных.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Task:
        """
        Получает задачу по ID из базы данных.
        """
        raise NotImplementedError
