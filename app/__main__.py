from fastapi import FastAPI

from implementations.task_storage import TaskStorage
from routes import HelloWorldRouter, RefreshTokenRouter
from routes.create_task_route import CreateTaskRouter
from routes.create_user_and_tokens import CreateUserAndTokensRouter
from routes.delete_task import DeleteTaskRouter
from routes.task_routes import TaskRouter
from routes.update_task import UpdateTaskRouter
from stubs.create_token import CreateTokenStub
from stubs.encrypter_stub import EncrypterStub
from stubs.token_storage_stub import TokenStorageStub
from stubs.user_storage_stub import UserStorageStub

app = FastAPI()

# Зависимости для Task-related маршрутов
task_storage = TaskStorage()

# Добавляем маршруты для задач
app.include_router(HelloWorldRouter().router)

app.include_router(
    RefreshTokenRouter(
        user_storage=UserStorageStub(),
        encrypter=EncrypterStub(),
        create_token=CreateTokenStub(),
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
user_storage = UserStorageStub()
token_storage = TokenStorageStub()
encrypter = EncrypterStub()
create_token = CreateTokenStub()
expire_days = 30

# Добавляем маршрут для создания пользователя и токенов
app.include_router(
    CreateUserAndTokensRouter(
        user_storage=user_storage,
        token_storage=token_storage,
        encrypter=encrypter,
        create_token=create_token,
        expire_days=expire_days,
    ).router
)
