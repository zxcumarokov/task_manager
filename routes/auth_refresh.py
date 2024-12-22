# auth_refr
import logging
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from abs import ITockenStorage, IUserStorage  # Интерфейсы хранилищ
from implementations.encrypter import FernetEncrypter  # Шифратор

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class RefreshTokenRequest(BaseModel):
    refresh_token: str  # Зашифрованный refresh токен


def create_refresh_router(
    token_storage: ITockenStorage,
    user_storage: IUserStorage,
    encrypter: FernetEncrypter,
):
    router = APIRouter()

    @router.post("/auth/refresh")
    async def refresh_access_token(request: RefreshTokenRequest):
        """
        Обновляет access токен пользователя, принимая зашифрованный refresh токен.
        """
        try:
            # Шаг 1: Дешифровать refresh токен
            try:
                logger.debug("Начинаем дешифрование refresh токена")
                decrypted_token = encrypter.decrypt(request.refresh_token)
                logger.debug(f"Расшифрованный токен: {decrypted_token}")
            except ValueError as e:
                logger.warning(f"Ошибка дешифрования токена: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid refresh token")

            # Шаг 2: Проверить формат токена (ожидается JWT токен)
            try:
                # Декодируем JWT токен
                decoded_token = jwt.decode(
                    decrypted_token, options={"verify_signature": False}
                )  # Не проверяем подпись
                username = decoded_token.get("username")
                expire_time = datetime.fromtimestamp(decoded_token.get("exp"))
                logger.debug(
                    f"JWT токен: username={username}, expire_time={expire_time}"
                )
            except jwt.ExpiredSignatureError:
                logger.warning("JWT токен истёк")
                raise HTTPException(status_code=400, detail="Refresh token expired")
            except jwt.InvalidTokenError as e:
                logger.warning(f"Некорректный JWT токен: {str(e)}")
                raise HTTPException(status_code=400, detail="Invalid token format")

            # Шаг 3: Проверить срок действия токена
            if expire_time < datetime.now():
                logger.warning("Refresh токен истёк")
                raise HTTPException(status_code=400, detail="Refresh token expired")

            # Шаг 4: Получить пользователя из хранилища
            user = await user_storage.get_user(username=username)
            if not user:
                logger.warning(f"Пользователь '{username}' не найден")
                raise HTTPException(status_code=404, detail="User not found")

            # Шаг 5: Генерация нового access токена
            new_access_token = await token_storage.create_access_token(
                username=username,
                expire_date_time=datetime.now() + timedelta(hours=1),
            )
            encrypted_access_token = encrypter.encrypt(new_access_token)

            # Шаг 6: Сохранение нового токена в базе данных
            logger.debug(f"Сохраняем новый access токен для пользователя '{username}'")
            user.encrypted_access_token = encrypted_access_token
            await token_storage.save_tokens(
                user
            )  # Обновляем запись пользователя в базе данных

            logger.info(f"Access токен обновлён для пользователя '{username}'")
            return {
                "message": "Access token refreshed successfully",
                "username": username,
                "encrypted_access_token": encrypted_access_token,
            }

        except HTTPException as http_exc:
            logger.warning(f"HTTP ошибка при обновлении токена: {http_exc.detail}")
            raise http_exc

        except Exception as e:
            logger.error(f"Неизвестная ошибка: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return router
