# Setup logging
import logging  # Add logging impor
import os
import secrets

from dotenv import load_dotenv
from fastapi import FastAPI

from implementations.encrypter import FernetEncrypter
from implementations.task_storage import TaskStorage
from implementations.token_storage import TokenStorage
from implementations.token_verifier import TokenVerifier  # Импортировать TokenVerifier
from implementations.user_storage import UserStorage
from routes import HelloWorldRouter
from routes.auth_login import create_login_router
from routes.auth_refresh import create_refresh_router
from routes.auth_register import create_user_router
from routes.create_task_route import CreateTaskRouter
from routes.delete_task import DeleteTaskRouter
from routes.task_routes import TaskRouter
from routes.update_task import UpdateTaskRouter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get SECRET_KEY from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")

# If SECRET_KEY is not found, generate a new one and save it to .env
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)  # Generate a random 256-bit key
    with open(".env", "a") as f:
        f.write(f"SECRET_KEY={SECRET_KEY}\n")

# Dependencies for Task-related routes
task_storage = TaskStorage(encrypter=FernetEncrypter())
gpg_home = os.getenv("GPG_HOME")
gpg_home = str(gpg_home)
database_url = os.getenv("DATABASE_URL")
database_url = str(database_url)

# Dependencies for authentication routes
user_storage = UserStorage()
token_storage = TokenStorage(database_url=database_url)
encrypter = FernetEncrypter()
expire_days = 30

# Create the token_verifier instance
token_verifier = TokenVerifier(
    secret_key=SECRET_KEY, encrypter=encrypter
)  # Создаем объект token_verifier

# Create FastAPI app
app = FastAPI()

# Add task-related routes
app.include_router(HelloWorldRouter().router)

app.include_router(
    TaskRouter(
        task_storage=task_storage,
    ).router
)

app.include_router(
    CreateTaskRouter(
        task_storage=task_storage,
        token_verifier=token_verifier,  # Передаем token_verifier
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

# Add user registration, login, and token refresh routes
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
