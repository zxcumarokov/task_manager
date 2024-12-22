# auth_register.py
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import IUserStorage
from implementations.encrypter import FernetEncrypter
from models.user import User

logger = logging.getLogger(__name__)


class CreateUserRequest(BaseModel):
    username: str
    password: str


def create_user_router(user_storage: IUserStorage, encrypter: FernetEncrypter):
    router = APIRouter()

    @router.post("/auth/register")
    async def register_user(request: CreateUserRequest):
        logger.info("Запрос на создание пользователя: %s", request.username)

        try:
            # Проверяем, существует ли пользователь
            try:
                existing_user = await user_storage.get_user(request.username)
                raise HTTPException(status_code=400, detail="User already exists")
            except ValueError:
                pass

            # Шифруем пароль
            encrypted_password = encrypter.encrypt(request.password)

            # Создаем нового пользователя
            user = User(
                username=request.username,
                encrypted_password=encrypted_password,
                encrypted_refresh_token=None,
                encrypted_access_token=None,
            )
            await user_storage.create_user(user)
            return {"message": "User successfully created", "username": user.username}

        except Exception as e:
            logger.error("Ошибка при создании пользователя: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return router
