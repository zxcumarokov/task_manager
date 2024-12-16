import os  # noqa

from fastapi import FastAPI

from implementations.encrypter import GPGEncrypter
from implementations.task_storage import TaskStorage
from implementations.token_storage import TokenStorage
from implementations.user_storage import UserStorage
from routes import HelloWorldRouter
from routes.auth_login import create_login_router
from routes.auth_refresh import create_refresh_router
from routes.auth_register import create_user_router
from routes.create_task_route import CreateTaskRouter
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

# Зависимости для маршрутов аутентификации
user_storage = UserStorage()
token_storage = TokenStorage(database_url=database_url)
encrypter = GPGEncrypter(gpg_home=gpg_home)
expire_days = 30

# Добавляем маршруты для задач
app.include_router(HelloWorldRouter().router)

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

# Зависимости для маршрутов аутентификации
user_storage = UserStorage()
token_storage = TokenStorage(database_url=database_url)
encrypter = GPGEncrypter(gpg_home=gpg_home)
expire_days = 30

# Добавляем маршруты для регистрации пользователя, входа и обновления токенов
app.include_router(
    create_user_router(
        user_storage=user_storage,
        encrypter=encrypter,
    )
)

app.include_router(
    create_login_router(
        token_storage=token_storage,
        user_storage=user_storage,
        encrypter=encrypter,
        expire_days=expire_days,
    )
)

app.include_router(
    create_refresh_router(
        token_storage=token_storage,
        user_storage=user_storage,
        encrypter=encrypter,
    )
)
