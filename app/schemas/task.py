from pydantic import BaseModel, ConfigDict


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    priority: int
    complete: bool
    user_id: int


class CreateTaskRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool


class UpdateTaskRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    complete: bool | None = None
