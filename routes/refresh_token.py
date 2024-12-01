from datetime import datetime, timedelta

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from abs import ICreateToken, IUserStorage
from implementations.encrypter import GPGEncrypter


class RefreshTokenRequest(BaseModel):
    username: str
    password: str


class RefreshTokenRouter:
    def __init__(
        self,
        user_storage: IUserStorage,
        encrypter: GPGEncrypter,
        create_token: ICreateToken,
        expire_days: int,
    ):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/create_refresh_token",
            endpoint=self.get_refresh_token,
            methods=["POST"],
        )
        self.user_storage = user_storage
        self.encrypter = encrypter
        self.create_token = create_token
        self.expire_days = expire_days

    async def get_refresh_token(self, request: RefreshTokenRequest):
        """
        Создает токен
        """

        user = await self.user_storage.get_user(request.username)
        user_password = self.encrypter.decrypt(user.encrypted_password)
        if str(user_password) != request.password:
            return JSONResponse(
                content={"error": "Invalid password"},
                status_code=401,
            )

        expire_date_time = datetime.now() + timedelta(days=self.expire_days)

        refresh_token = self.create_token.create_token(
            username=user.username,
            expire_date_time=expire_date_time,
        )
        return JSONResponse(
            content={"refresh_token": refresh_token},
            status_code=200,
        )
