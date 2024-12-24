#
from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException

from implementations.encrypter import FernetEncrypter
from implementations.token_verifier import TokenVerifier

SECRET_KEY = "gAAAAABnZ2vLeB-DsDnwxZlwgw4I5RlHYxT67YynPWmF-D0J0eOlg-gmZFKLSLNhSNw6RclWFOunvMQZrDDgHoYoaUrOjzt8OeXrW-Fd-tg9Y5DfL3AwbqYhh26yv4vnMbn70zTqunUYBbOlseGkEf67VvfF7n6TgJsuqG7y9u6zJMmz6Qj4Tyr3VQRlczCLO5UANcg9ntmJHchdGf1HsFpDvTKo-rl-TX1yd2IXqh50r9a20sXG3Fc="
FERNET_KEY = "E8ooGyS9li9seXtSeRzGBf7x-RrKG69xcD3fEgYGuUo="  # Замените на ваш актуальный ключ Fernet

encrypter = FernetEncrypter()


def test_verify_token_with_expired_token():
    """
    Тест для проверки истёкшего токена.
    """
    expired_token = "gAAAAABnZ2vLeB-DsDnwxZlwgw4I5RlHYxT67YynPWmF-D0J0eOlg-gmZFKLSLNhSNw6RclWFOunvMQZrDDgHoYoaUrOjzt8OeXrW-Fd-tg9Y5DfL3AwbqYhh26yv4vnMbn70zTqunUYBbOlseGkEf67VvfF7n6TgJsuqG7y9u6zJMmz6Qj4Tyr3VQRlczCLO5UANcg9ntmJHchdGf1HsFpDvTKo-rl-TX1yd2IXqh50r9a20sXG3Fc="
    token_verifier = TokenVerifier(SECRET_KEY, encrypter)

    with pytest.raises(HTTPException) as exc_info:
        token_verifier.verify_token(expired_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token expired. Please refresh your token."


def test_verify_token_with_invalid_token():
    """
    Тест для проверки невалидного токена.
    """
    invalid_token = "invalid_token_example"
    token_verifier = TokenVerifier(SECRET_KEY, encrypter)

    with pytest.raises(HTTPException) as exc_info:
        token_verifier.verify_token(invalid_token)

    assert exc_info.value.status_code == 400  # Ошибка при формате токена
    assert exc_info.value.detail == "Invalid token format or decryption error"


def test_verify_token_with_valid_token():
    """
    Тест для проверки валидного токена.
    """
    valid_token = "gAAAAABnZ2vLeB-DsDnwxZlwgw4I5RlHYxT67YynPWmF-D0J0eOlg-gmZFKLSLNhSNw6RclWFOunvMQZrDDgHoYoaUrOjzt8OeXrW-Fd-tg9Y5DfL3AwbqYhh26yv4vnMbn70zTqunUYBbOlseGkEf67VvfF7n6TgJsuqG7y9u6zJMmz6Qj4Tyr3VQRlczCLO5UANcg9ntmJHchdGf1HsFpDvTKo-rl-TX1yd2IXqh50r9a20sXG3Fc="
    token_verifier = TokenVerifier(SECRET_KEY, encrypter)

    user_id = token_verifier.verify_token(valid_token)

    assert (
        user_id == "12345"
    )  # Здесь вы можете заменить на ожидаемый user_id, если он отличается от 12345
