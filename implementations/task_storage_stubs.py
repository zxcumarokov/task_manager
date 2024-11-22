from abs.abc_task_storage import ITaskStorage
from models import Task


class TaskStorageStubs(ITaskStorage):
    def __init__(self):
        # Счётчик для генерации уникальных идентификаторов задач
        self.current_id = 1

    def create_task(self, task: Task) -> int:
        # Присваиваем новый уникальный ID
        task_id = self.current_id
        self.current_id += 1
        return task_id

    def upgrade_task(self, task: Task, task_id: int) -> None:
        pass

    def delete_task(self, task: Task, task_id: int) -> None:
        pass

    def get_task_by_id(self, id: int) -> Task:
        return Task(
            id=id,
            title="title",
            description="description",
            status="status",
        )
