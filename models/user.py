from pydantic import BaseModel


class User(BaseModel):
    username: str
    encrypted_password: str
    encrypted_refresh_token: str | None
    encrypted_access_token: str | None
