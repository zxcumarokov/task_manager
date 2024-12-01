import os

import gnupg

from abs import IEncrypter


class GPGEncrypter(IEncrypter):
    def __init__(self, gpg_home: str):
        """
        Инициализация шифровщика с использованием GPG.
        :param gpg_home: Директория для хранения GPG-ключей.
        """
        self.gpg = gnupg.GPG(gnupghome=gpg_home)  # Указываем директорию с ключами
        self.key_id = os.getenv("GPG_KEY_ID")  # Загружаем идентификатор ключа из .env
        if not self.key_id:
            raise ValueError("GPG_KEY_ID не указан в .env файле")

    def encrypt(self, password: str) -> str:
        """
        Шифрует переданный пароль.
        :param password: Пароль для шифрования.
        :return: Зашифрованная строка.
        """
        encrypted_data = self.gpg.encrypt(password, self.key_id)
        if not encrypted_data.ok:
            raise ValueError(f"Ошибка шифрования: {encrypted_data.status}")
        return str(encrypted_data)  # Возвращаем зашифрованный текст

    def decrypt(self, encrypted_password: str) -> str:
        """
        Дешифрует переданную строку.
        :param encrypted_password: Зашифрованная строка.
        :return: Исходный пароль.
        """
        decrypted_data = self.gpg.decrypt(encrypted_password)
        if not decrypted_data.ok:
            raise ValueError(f"Ошибка дешифрования: {decrypted_data.status}")
        return str(decrypted_data)  # Возвращаем расшифрованный текст
