from abs import IUserStorage
from models import User


class UserStorageStub(IUserStorage):
    async def get_user(self, username: str) -> User:
        return User(
            username=username,
            encrypted_password="password",
            encripted_refresh_token="refresh_token",
            encripted_access_token="access_token",
        )
