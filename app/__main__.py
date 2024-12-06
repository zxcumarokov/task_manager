import os  # noqa

import dotenv  # noqa
from fastapi import FastAPI

from implementations.encrypter import GPGEncrypter
from implementations.task_storage import TaskStorage
from implementations.token_storage import TokenStorage
from implementations.user_storage import UserStorage
from routes import HelloWorldRouter, RefreshTokenRouter
from routes.create_task_route import CreateTaskRouter
from routes.create_user_and_tokens import CreateUserAndTokensRouter
from routes.delete_task import DeleteTaskRouter
from routes.task_routes import TaskRouter
from routes.update_task import UpdateTaskRouter

app = FastAPI()

# Зависимости для Task-related маршрутов
task_storage = TaskStorage()
gpg_home = os.getenv("GPG_HOME")
gpg_home = str(gpg_home)
database_url = os.getenv("DATABASE_URL")
database_url = str(database_url)
# Добавляем маршруты для задач
app.include_router(HelloWorldRouter().router)

app.include_router(
    RefreshTokenRouter(
        user_storage=UserStorage(),
        encrypter=GPGEncrypter(gpg_home=gpg_home),
        token_storage=TokenStorage(database_url=database_url),
        expire_days=100,
    ).router
)

app.include_router(
    TaskRouter(
        task_storage=task_storage,
    ).router
)

app.include_router(
    CreateTaskRouter(
        task_storage=task_storage,
    ).router
)

app.include_router(
    UpdateTaskRouter(
        task_storage=task_storage,
    ).router
)

app.include_router(
    DeleteTaskRouter(
        task_storage=task_storage,
    ).router
)

# Зависимости для CreateUserAndTokensRouter
user_storage = UserStorage()
token_storage = TokenStorage(database_url=database_url)
encrypter = GPGEncrypter(gpg_home=gpg_home)
expire_days = 30

# Добавляем маршрут для создания пользователя и токенов
app.include_router(
    CreateUserAndTokensRouter(
        user_storage=user_storage,
        token_storage=token_storage,
        encrypter=encrypter,
        expire_days=expire_days,
    ).router
)
