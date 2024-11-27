from abs import IEncrypter


class EncrypterStub(IEncrypter):
    def encrypt(self, password: str) -> str:
        return "encrypted_password"

    def decrypt(self, encrypted_password: str) -> str:
        return "password"
