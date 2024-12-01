from fastapi import APIRouter, HTTPException

from abs import ITaskStorage
from models import Task


class CreateTaskRouter:
    def __init__(self, task_storage: ITaskStorage):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_task",
            endpoint=self.create_task,
            methods=["POST"],
        )
        self.task_storage = task_storage

    async def create_task(self, new_task: Task):
        """Создает задачу в базе данных на основе данных из запроса."""
        try:
            task_id = await self.task_storage.create_task(new_task)  # Добавлен await
            new_task.id = task_id
            return {"message": "Task created successfully", "task": new_task}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
