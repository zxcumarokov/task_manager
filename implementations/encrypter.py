import logging
import os

import gnupg

from abs import IEncrypter

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GPGEncrypter(IEncrypter):
    def __init__(self, gpg_home: str):
        """
        Инициализация шифровщика с использованием GPG.
        :param gpg_home: Директория для хранения GPG-ключей.
        """
        self.gpg = gnupg.GPG(
            homedir=gpg_home, binary="/usr/local/bin/gpg"
        )  # Указываем директорию с ключами
        self.key_id = os.getenv("GPG_KEY_ID")  # Загружаем идентификатор ключа из .env
        if not self.key_id:
            raise ValueError("GPG_KEY_ID не указан в .env файле")
        logger.debug(f"GPG ключ загружен: {self.key_id}")

    def encrypt(self, password: str) -> str:
        """
        Шифрует переданный пароль.
        :param password: Пароль для шифрования.
        :return: Зашифрованная строка.
        """
        logger.debug(f"Начало шифрования пароля: {password}")
        encrypted_data = self.gpg.encrypt(password, self.key_id)
        if not encrypted_data.ok:
            logger.error(f"Ошибка шифрования: {encrypted_data.status}")
            raise ValueError(f"Ошибка шифрования: {encrypted_data.status}")
        logger.debug(f"Пароль зашифрован: {str(encrypted_data)}")
        return str(encrypted_data)  # Возвращаем зашифрованный текст

    def decrypt(self, encrypted_password: str) -> str:
        """
        Дешифрует переданную строку.
        :param encrypted_password: Зашифрованная строка.
        :return: Исходный пароль.
        """
        logger.debug(f"Начало дешифрования сообщения: {encrypted_password}")
        logger.debug(f"Используемый GPG ключ: {self.key_id}")

        decrypted_data = self.gpg.decrypt(encrypted_password)
        if not decrypted_data.ok:
            logger.error(f"Ошибка дешифрования: {decrypted_data.status}")
            raise ValueError(f"Ошибка дешифрования: {decrypted_data.status}")

        logger.debug(f"Дешифрованное сообщение: {str(decrypted_data)}")
        return str(decrypted_data)
