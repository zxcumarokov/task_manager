from abc import ABC, abstractmethod
from typing import List, Optional

from models import Task


class ITaskStorage(ABC):
    @abstractmethod
    async def create_task(self, task: Task, token: str) -> int:
        """
        Создаёт новую задачу и возвращает её ID.
        :param task: Задача, которую нужно создать.
        :param token: Токен, используемый для авторизации.
        :return: ID созданной задачи.
        """
        raise NotImplementedError

    @abstractmethod
    async def upgrade_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        """
        Обновляет задачу в базе данных.
        Можно передать одно или несколько полей (title, description, status).
        :param task_id: ID задачи, которую нужно обновить.
        :param title: Новый заголовок задачи (необязательный).
        :param description: Новое описание задачи (необязательное).
        :param status: Новый статус задачи (необязательный).
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу из базы данных.
        :param task_id: ID задачи, которую нужно удалить.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, task_id: int) -> Task:
        """
        Получает задачу по ID из базы данных.
        :param task_id: ID задачи, которую нужно получить.
        :return: Задача с указанным ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_user_id(self, user_id: int) -> List[Task]:
        """
        Возвращает список задач, связанных с пользователем.
        :param user_id: ID пользователя, чьи задачи нужно получить.
        :return: Список задач, связанных с пользователем.
        """
        raise NotImplementedError
