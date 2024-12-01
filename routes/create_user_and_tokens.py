from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import ITokenStorage, IUserStorage
from implementations.encrypter import GPGEncrypter
from models.user import User


class CreateUserRequest(BaseModel):
    username: str
    password: str


class CreateUserAndTokensRouter:
    def __init__(
        self,
        user_storage: IUserStorage,
        token_storage: ITokenStorage,
        encrypter: GPGEncrypter,
        create_token,  # Экземпляр ICreateToken
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
        self.create_token = create_token
        self.expire_days = expire_days

    async def create_user_and_tokens(self, request: CreateUserRequest):
        """Создает пользователя и токены."""
        try:
            # Проверяем, существует ли пользователь
            existing_user = await self.user_storage.get_user(request.username)
            if existing_user:
                raise HTTPException(status_code=400, detail="User already exists")

            # Шифруем пароль
            encrypted_password = self.encrypter.encrypt(request.password)

            # Создаем пользователя
            user = User(
                username=request.username,
                encrypted_password=encrypted_password,
                encrypted_refresh_token=None,
                encrypted_access_token=None,
            )
            await self.user_storage.create_user(user)

            # Генерация токенов
            expire_date_time = datetime.now() + timedelta(days=self.expire_days)

            refresh_token = self.create_token.create_token(
                username=user.username,
                expire_date_time=expire_date_time,
            )
            access_token = self.create_token.create_token(
                username=user.username,
                expire_date_time=datetime.now() + timedelta(hours=1),  # На 1 час
            )

            # Шифруем токены
            encrypted_refresh_token = self.encrypter.encrypt(refresh_token)
            encrypted_access_token = self.encrypter.encrypt(access_token)

            # Обновляем данные пользователя
            user.encrypted_refresh_token = encrypted_refresh_token
            user.encrypted_access_token = encrypted_access_token

            # Сохраняем токены в базе данных
            await self.token_storage.save_tokens(user)

            return {
                "message": "User and tokens created successfully",
                "user": {
                    "username": user.username,
                    "encrypted_refresh_token": encrypted_refresh_token,
                    "encrypted_access_token": encrypted_access_token,
                },
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
