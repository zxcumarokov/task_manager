from fastapi import APIRouter, HTTPException

from implementations.task_storage import TaskStorage


class TaskRouter:
    def __init__(self, task_storage: TaskStorage):
        self.router = APIRouter()
        self.task_storage = task_storage

        # Регистрация маршрута
        self.router.add_api_route(
            path="/get_task_by_id/{task_id}",
            endpoint=self.get_task_by_id,
            methods=["GET"],
        )

    async def get_task_by_id(self, task_id: int):
        """
        Получает задачу по ID
        """
        try:
            task = await self.task_storage.get_task_by_id(task_id)
            task_dict = task.model_dump()  # Преобразуем модель в словарь
            return task_dict
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="An unexpected error occurred")
