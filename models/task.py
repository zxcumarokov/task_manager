from pydantic import BaseModel


class Task(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    status: str | None = None
