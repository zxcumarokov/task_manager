from fastapi import APIRouter, HTTPException

from abs.abc_task_storage import ITaskStorage


class DeleteTaskRouter:
    def __init__(self, task_storage: ITaskStorage):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/delete_task/{task_id}", endpoint=self.delete_task, methods=["DELETE"]
        )
        self.task_storage = task_storage

    async def delete_task(self, task_id: int):
        """Удаляет задачу из базы данных по ее ID."""
        try:
            # Удаление задачи
            await self.task_storage.delete_task(task_id)
            return {"message": f"Task with ID {task_id} deleted successfully"}
        except ValueError:
            # Ошибка, если задача не найдена
            raise HTTPException(
                status_code=404, detail=f"Task with ID {task_id} not found"
            )
        except Exception:
            # Неопределенная ошибка
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
