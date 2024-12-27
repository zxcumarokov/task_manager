import logging

from fastapi import APIRouter, Header, HTTPException

from abs import ITaskStorage, ITokenVerifier
from models import Task

logger = logging.getLogger(__name__)


class CreateTaskRouter:
    def __init__(
        self,
        task_storage: ITaskStorage,
        token_verifier: ITokenVerifier,
    ):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_task",
            endpoint=self.create_task,
            methods=["POST"],
        )
        self.task_storage = task_storage
        self.token_verifier = token_verifier

    async def create_task(self, new_task: Task, x_token: str = Header(...)):
        """
        Создаёт новую задачу для пользователя, валидируя токен.

        :param new_task: Новая задача, созданная пользователем.
        :param x_token: Токен для авторизации.
        :return: Информация о созданной задаче.
        """
        logger.debug(f"Received request to create task with data: {new_task.dict()}")

        # Проверяем токен и получаем user_id
        try:
            user_id = self.token_verifier.verify_token(x_token)
            logger.debug(f"Verified user_id: {user_id}")
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        try:
            logger.debug(f"Assigning user_id {user_id} to the task")
            new_task.user_id = int(user_id)  # Преобразование строки в число

            # Сохраняем задачу в хранилище
            task_id = await self.task_storage.create_task(new_task, x_token)
            new_task.id = task_id
            logger.debug(f"Task created successfully with ID: {task_id}")

            return {"message": "Task created successfully", "task": new_task}
        except ValueError as e:
            logger.error(f"Invalid user_id format: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid user_id format")
        except Exception as e:
            logger.error(f"Error occurred during task creation: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
