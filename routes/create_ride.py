from fastapi import APIRouter, HTTPException

from abs import ITaskStorage  # Импортируем интерфейс для хранения задач
from models.task import Task  # Импортируем модель Task


class CreateRide:
    def __init__(self, task_storage: ITaskStorage):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_ride",
            endpoint=self.create_ride,
            methods=["POST"],
        )
        self.task_storage = task_storage

    async def create_ride(self, new_ride: Task):
        """
        Создает поездку (задачу) в базе данных на основе данных из запроса.
        """
        try:
            ride_id = await self.task_storage.create_task(
                new_ride
            )  # Используем интерфейс для хранения задачи
            new_ride.id = ride_id
            return {"message": "Ride created successfully", "ride": new_ride}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
