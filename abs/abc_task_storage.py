from abc import ABC, abstractmethod

from models import Task


class ITaskStorage(ABC):
    @abstractmethod
    def create_task(self, task: Task):
        """
        Create a new task and return its ID
        """
        raise NotImplementedError

    @abstractmethod
    def upgrade_task(
        self,
        task_id: int,
        title: str,
        description: str,
        status: str,
    ) -> None:
        """
        Update a task
        """
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task: Task, task_id: int) -> None:
        """
        Delete a task
        """
        raise NotImplementedError

    @abstractmethod
    def get_task_by_id(self, id: int) -> Task:
        """
        Get a task by ID
        """
        raise NotImplementedError
