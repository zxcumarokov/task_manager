from datetime import datetime

from abs import ICreateToken


class CreateTokenStub(ICreateToken):
    def create_token(self, id: int, Expiration: datetime) -> str:
        return "token"
