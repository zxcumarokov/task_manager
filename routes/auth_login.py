import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import ITockenStorage, IUserStorage
from implementations.encrypter import GPGEncrypter

logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    username: str
    password: str


def create_login_router(
    user_storage: IUserStorage,
    token_storage: ITockenStorage,
    encrypter: GPGEncrypter,
    expire_days: int,
):
    router = APIRouter()

    @router.post("/auth/login")
    async def login_user(request: LoginRequest):
        try:
            # Извлечение данных из тела запроса
            username = request.username
            password = request.password

            # Получение пользователя из хранилища
            user = await user_storage.get_user(username)

            # Проверка пароля
            if not encrypter.decrypt(user.encrypted_password) == password:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            # Создание токенов с заданным временем жизни
            expire_access_token = datetime.now() + timedelta(hours=1)
            expire_refresh_token = datetime.now() + timedelta(days=expire_days)

            # Создание refresh токена
            refresh_token = await token_storage.create_refresh_token(
                username=user.username
            )

            # Создание access токена
            access_token = await token_storage.create_access_token(
                username=user.username,
                expire_date_time=expire_access_token,
            )

            # Шифрование токенов
            encrypted_refresh_token = encrypter.encrypt(refresh_token)
            encrypted_access_token = encrypter.encrypt(access_token)

            # Сохранение токенов у пользователя
            user.encrypted_refresh_token = encrypted_refresh_token
            user.encrypted_access_token = encrypted_access_token
            await token_storage.save_tokens(user)

            # Успешный ответ
            return {
                "message": "Login successful",
                "username": user.username,
                "encrypted_refresh_token": encrypted_refresh_token,
                "encrypted_access_token": encrypted_access_token,
            }
        except Exception as e:
            logger.error("Ошибка при входе пользователя: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return router
