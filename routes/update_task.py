from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import ITaskStorage


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


class UpdateTaskRouter:
    def __init__(self, task_storage: ITaskStorage):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/update_task/{task_id}",
            endpoint=self.update_task,
            methods=["POST"],
        )
        self.task_storage = task_storage

    async def update_task(self, task_id: int, task_update: TaskUpdate):
        """
        Обновляет задачу в базе данных на основе данных из запроса.
        """
        try:
            await self.task_storage.upgrade_task(  # Добавлен await
                task_id=task_id,
                title=task_update.title,
                description=task_update.description,
                status=task_update.status,
            )
            return {"message": "Task updated successfully", "task_id": task_id}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception:
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
