import logging
import os

from cryptography.fernet import Fernet

from abs import IEncrypter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FernetEncrypter(IEncrypter):
    KEY_FILE = "fernet.key"  # Имя файла для хранения ключа

    def __init__(self):
        """
        Инициализация шифровщика с использованием Fernet.
        Если ключ отсутствует, он будет загружен из файла или создан.
        """
        if os.path.exists(self.KEY_FILE):
            # Загружаем ключ из файла
            with open(self.KEY_FILE, "rb") as file:
                self.key = file.read()
            logger.debug("Ключ Fernet загружен из файла.")
        else:
            # Генерация нового ключа и сохранение его в файл
            self.key = Fernet.generate_key()
            with open(self.KEY_FILE, "wb") as file:
                file.write(self.key)
            logger.warning(
                f"Ключ Fernet не найден. Создан и сохранён в файл {self.KEY_FILE}"
            )

        self.fernet = Fernet(self.key)

    def encrypt(self, password: str) -> str:
        """
        Шифрует переданный пароль.
        :param password: Пароль для шифрования.
        :return: Зашифрованная строка.
        """
        logger.debug(f"Начало шифрования пароля.")
        encrypted_data = self.fernet.encrypt(password.encode())
        encrypted_str = encrypted_data.decode()
        logger.debug(f"Пароль зашифрован.")
        return encrypted_str

    def decrypt(self, encrypted_password: str) -> str:
        """
        Дешифрует переданную строку.
        :param encrypted_password: Зашифрованная строка.
        :return: Исходный пароль.
        """
        logger.debug(f"Начало дешифрования сообщения.")
        try:
            decrypted_data = self.fernet.decrypt(encrypted_password.encode())
            decrypted_str = decrypted_data.decode()
            logger.debug(f"Дешифрованное сообщение.")
            return decrypted_str
        except Exception as e:
            logger.error(f"Ошибка при дешифровке: {e}")
            raise ValueError("Invalid encrypted message") from e
