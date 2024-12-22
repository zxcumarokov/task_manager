import logging
from datetime import datetime

import jwt
from fastapi import APIRouter, Header, HTTPException

from abs import ITaskStorage
from implementations.encrypter import FernetEncrypter
from models import Task

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CreateTaskRouter:
    def __init__(
        self, task_storage: ITaskStorage, secret_key: str, encrypter: FernetEncrypter
    ):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_task",
            endpoint=self.create_task,
            methods=["POST"],
        )
        self.task_storage = task_storage
        self.secret_key = secret_key  # Секретный ключ для проверки токенов
        self.encrypter = encrypter

    def _verify_token(self, token: str):
        try:
            logger.debug(f"Verifying token: {token}")
            decrypted_token = self.encrypter.decrypt(token)
            logger.debug(f"Decrypted token: {decrypted_token}")
            decoded_token = jwt.decode(
                decrypted_token, self.secret_key, algorithms=["HS256"]
            )
            user_id = decoded_token.get("user_id")
            exp = decoded_token.get("exp")
            logger.debug(f"Decoded token: {decoded_token}")
            if not user_id:
                raise HTTPException(
                    status_code=401, detail="User ID not found in token"
                )
            if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=401, detail="Token expired. Please refresh your token."
                )
            return user_id
        except jwt.ExpiredSignatureError:
            logger.error("Token expired")
            raise HTTPException(
                status_code=401, detail="Token expired. Please refresh your token."
            )
        except jwt.PyJWTError as e:
            logger.error(f"JWT error: {str(e)}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except ValueError as e:
            logger.error(f"Decryption or token parsing failed: {str(e)}")
            raise HTTPException(
                status_code=400, detail="Invalid token format or decryption error"
            )

    async def create_task(self, new_task: Task, x_token: str = Header(...)):
        logger.debug(f"Received request to create task with data: {new_task.dict()}")

        user_id = self._verify_token(x_token)

        try:
            logger.debug(f"Assigning user_id {user_id} to the task")
            new_task.user_id = user_id
            task_id = await self.task_storage.create_task(new_task, x_token)
            new_task.id = task_id
            logger.debug(f"Task created successfully with ID: {task_id}")
            return {"message": "Task created successfully", "task": new_task}
        except Exception as e:
            logger.error(f"Error occurred during task creation: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
