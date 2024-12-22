from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    status: str
    user_id: Optional[int] = None  # Это будет заполняться в процессе создания
    id: Optional[int] = None  # ID будет присваиваться после сохранения задачи
