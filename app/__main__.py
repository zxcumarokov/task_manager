from typing import Union

from fastapi import FastAPI

from implementations.task_storage import TaskStorage
from models import Task

app = FastAPI()
task_storage = TaskStorage()
from typing import Optional

from pydantic import BaseModel


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_task_by_id/{task_id}")
def read_item(
    task_id: int,
):
    task = task_storage.get_task_by_id(task_id)
    task_dict = task.model_dump()

    return task_dict


@app.post("/create_task")
def create_task(new_task: Task):
    """Создает задачу в базе данных на основе данных из запроса."""
    # Добавляем задачу в базу
    task_id = task_storage.create_task(new_task)
    new_task.id = task_id
    return {"message": "Task created successfully", "task": new_task}


@app.post("/update_task/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Обновляет задачу в базе данных на основе данных из запроса.
    """
    # Передаем данные в метод обновления
    task_storage.upgrade_task(
        task_id=task_id,
        title=task_update.title,
        description=task_update.description,
        status=task_update.status,
    )
    return {"message": "Task updated successfully", "task_id": task_id}
