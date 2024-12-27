from datetime import datetime, timedelta

import jwt
import pytest
from fastapi import HTTPException

from implementations.encrypter import FernetEncrypter
from implementations.token_verifier import TokenVerifier


@pytest.fixture
def encrypter():
    # Возвращаем фикстуру шифратора
    return FernetEncrypter()


@pytest.fixture
def token_verifier(encrypter):
    secret_key = "3b9d7a8df4e2d93ef7e6c64c2c4c8d3e7c67a9fa01b2e9d7e8f4e5b9c8d1a3f4"
    return TokenVerifier(secret_key, encrypter)


def test_verify_valid_token(token_verifier, encrypter):
    user_id = "user_123"

    # Создаем JWT токен
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user_id, "exp": expiration},
        token_verifier.secret_key,
        algorithm="HS256",
    )

    # Шифруем токен
    encrypted_token = encrypter.encrypt(token)

    # Проверяем, что токен валидный и расшифровывается правильно
    decoded_user_id = token_verifier.verify_token(encrypted_token)

    assert decoded_user_id == user_id


def test_token_expired(token_verifier, encrypter):
    user_id = "user_123"

    # Создаем JWT токен с истекшим сроком действия
    expiration = datetime.utcnow() - timedelta(hours=1)  # Истекший токен
    token = jwt.encode(
        {"user_id": user_id, "exp": expiration},
        token_verifier.secret_key,
        algorithm="HS256",
    )

    # Шифруем токен
    encrypted_token = encrypter.encrypt(token)

    # Проверяем, что выбрасывается исключение ExpiredSignatureError
    with pytest.raises(HTTPException) as exc_info:
        token_verifier.verify_token(encrypted_token)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Token expired. Please refresh your token."


def test_invalid_token_format(token_verifier, encrypter):
    # Передаем некорректный токен
    invalid_token = "invalid_token_format"

    # Проверяем, что выбрасывается исключение Invalid token format or decryption error
    with pytest.raises(HTTPException) as exc_info:
        token_verifier.verify_token(invalid_token)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid token format or decryption error"


def test_missing_user_id_in_token(token_verifier, encrypter):
    # Создаем JWT токен без user_id
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"exp": expiration}, token_verifier.secret_key, algorithm="HS256"
    )

    # Шифруем токен
    encrypted_token = encrypter.encrypt(token)

    # Проверяем, что выбрасывается исключение Token does not contain user_id
    with pytest.raises(HTTPException) as exc_info:
        token_verifier.verify_token(encrypted_token)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Token does not contain user_id"
