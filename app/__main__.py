from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from implementations.task_storage import TaskStorage
from models.task import Task
from routes import HelloWorldRouter, RefreshTokenRouter
from routes.create_ride import CreateRide
from routes.task_routes import TaskRouter
from stubs.create_token import CreateTokenStub
from stubs.encrypter_stub import EncrypterStub
from stubs.user_storage_stub import UserStorageStub

app = FastAPI()
task_storage = TaskStorage()  # Убедитесь, что TaskStorage поддерживает асинхронность
task_storage = TaskStorage()

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
    CreateRide(
        task_storage=task_storage,
    ).router
)

app.include_router
(
    TaskRouter(
        task_storage=task_storage,
    ).router
)


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


#
# @app.get("/get_task_by_id/{task_id}")
# async def read_item(task_id: int):
#     """Получает задачу по ID."""
#     try:
#         task = await task_storage.get_task_by_id(task_id)  # Добавлен await
#         task_dict = task.model_dump()  # Модификация, чтобы отобразить данные задачи
#         return task_dict
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="An unexpected error occurred")
#


@app.post("/create_task")
async def create_task(new_task: Task):
    """Создает задачу в базе данных на основе данных из запроса."""
    try:
        task_id = await task_storage.create_task(new_task)  # Добавлен await
        new_task.id = task_id
        return {"message": "Task created successfully", "task": new_task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_task/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Обновляет задачу в базе данных на основе данных из запроса.
    """
    try:
        await task_storage.upgrade_task(  # Добавлен await
            task_id=task_id,
            title=task_update.title,
            description=task_update.description,
            status=task_update.status,
        )
        return {"message": "Task updated successfully", "task_id": task_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@app.delete("/delete_task/{task_id}")
async def delete_task(task_id: int):
    """Удаляет задачу из базы данных по ее ID."""
    try:
        await task_storage.delete_task(task_id)  # Добавлен await
        return {"message": f"Task with ID {task_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@app.get("/task/{task_id}")
async def get_task(task_id: int):
    """
    Получает задачу из базы данных по ID.
    """
    try:
        task = await task_storage.get_task_by_id(task_id)  # Добавлен await
        return {"task": task}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
