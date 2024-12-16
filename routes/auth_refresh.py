# auth_refresh.p
# auth_refresh.py
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from abs import ITockenStorage, IUserStorage
from implementations.encrypter import GPGEncrypter
from models.user import User

logger = logging.getLogger(__name__)


def create_refresh_router(
    token_storage: ITockenStorage, user_storage: IUserStorage, encrypter: GPGEncrypter
):
    router = APIRouter()

    @router.post("/auth/refresh")
    async def refresh_access_token(refresh_token: str):
        try:
            decrypted_refresh_token = encrypter.decrypt(refresh_token)
            username, expire_time_str = decrypted_refresh_token.split(":")
            expire_time = datetime.strptime(expire_time_str, "%Y-%m-%d %H:%M:%S")

            if expire_time < datetime.now():
                raise HTTPException(status_code=400, detail="Refresh token expired")

            new_access_token = await token_storage.create_token(
                username=username, expire_date_time=datetime.now() + timedelta(hours=1)
            )

            encrypted_access_token = encrypter.encrypt(new_access_token)

            user = await user_storage.get_user(username=username)
            user.encrypted_access_token = encrypted_access_token

            await token_storage.save_tokens(user)

            return {
                "message": "Access token refreshed successfully",
                "username": username,
                "encrypted_access_token": encrypted_access_token,
            }

        except Exception as e:
            logger.error("Ошибка при обновлении токена: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return router
