import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import ITockenStorage, IUserStorage
from implementations.encrypter import GPGEncrypter
from models.user import User

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CreateUserRequest(BaseModel):
    username: str
    password: str


class CreateUserAndTokensRouter:
    def __init__(
        self,
        user_storage: IUserStorage,
        token_storage: ITockenStorage,
        encrypter: GPGEncrypter,
        expire_days: int,
    ):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_user_and_tokens",
            endpoint=self.create_user_and_tokens,
            methods=["POST"],
        )
        self.user_storage = user_storage
        self.token_storage = token_storage
        self.encrypter = encrypter
        self.expire_days = expire_days

    async def create_user_and_tokens(self, request: CreateUserRequest):
        """Создает пользователя и токены."""
        logger.info("Запрос на создание пользователя: %s", request.username)

        try:
            # Проверяем, существует ли пользователь
            logger.info(
                "Проверяем, существует ли пользователь с именем: %s", request.username
            )
            try:
                existing_user = await self.user_storage.get_user(request.username)
                logger.info(
                    "Пользователь %s найден: продолжаем обновление токенов",
                    request.username,
                )
            except ValueError:
                logger.info(
                    "Пользователь %s не найден: создаем нового", request.username
                )

                # Шифруем пароль
                logger.info(
                    "Шифруем пароль для нового пользователя: %s", request.username
                )
                encrypted_password = self.encrypter.encrypt(request.password)

                # Создаем нового пользователя
                user = User(
                    username=request.username,
                    encrypted_password=encrypted_password,
                    encrypted_refresh_token=None,
                    encrypted_access_token=None,
                )
                await self.user_storage.create_user(user)
                logger.info("Новый пользователь %s успешно создан", request.username)

                existing_user = user  # Используем нового пользователя

            # Генерация токенов
            logger.info("Генерация токенов для пользователя: %s", request.username)
            expire_date_time = datetime.now() + timedelta(days=self.expire_days)

            refresh_token = self.token_storage.create_token(
                username=existing_user.username,
                expire_date_time=expire_date_time,
            )
            access_token = self.token_storage.create_token(
                username=existing_user.username,
                expire_date_time=datetime.now() + timedelta(hours=1),  # На 1 час
            )
            logger.info(
                "Токены успешно сгенерированы для пользователя: %s", request.username
            )

            # Шифруем токены
            logger.info("Шифруем токены для пользователя: %s", request.username)
            encrypted_refresh_token = self.encrypter.encrypt(await refresh_token)
            encrypted_access_token = self.encrypter.encrypt(await access_token)

            # Обновляем данные пользователя
            existing_user.encrypted_refresh_token = encrypted_refresh_token
            existing_user.encrypted_access_token = encrypted_access_token

            # Сохраняем токены в базе данных
            logger.info("Сохраняем токены для пользователя: %s", request.username)
            await self.token_storage.save_tokens(existing_user)
            logger.info(
                "Токены успешно сохранены для пользователя: %s", request.username
            )

            return {
                "message": "User and tokens created successfully",
                "user": {
                    "username": existing_user.username,
                    "encrypted_refresh_token": encrypted_refresh_token,
                    "encrypted_access_token": encrypted_access_token,
                },
            }
        except Exception as e:
            logger.error(
                "Ошибка при создании пользователя или токенов: %s",
                str(e),
                exc_info=True,
            )
            raise HTTPException(status_code=500, detail=str(e))
