from abs.abc_inserttoken import ITokenStorage
from models.user import User


class TokenStorage(ITokenStorage):
    def __init__(self, database_client):
        """Инициализирует хранилище с клиентом базы данных."""
        self.database_client = database_client

    async def save_tokens(self, user: User) -> None:
        """Сохраняет токены пользователя в базу данных."""
        query = """
        UPDATE users
        SET encrypted_refresh_token = :refresh_token,
            encrypted_access_token = :access_token
        WHERE username = :username
        """
        await self.database_client.execute(
            query,
            {
                "username": user.username,
                "refresh_token": user.encrypted_refresh_token,
                "access_token": user.encrypted_access_token,
            },
        )
