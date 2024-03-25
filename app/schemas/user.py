from datetime import date, datetime, time, timedelta
from pydantic import BaseModel, EmailStr

from app.schemas.task import TaskOut


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    created_at: datetime
    updated_at: datetime


class UserToken(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    role: str


class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None
    role: str | None = None


class UserWithTasks(User):
    tasks: list[TaskOut] = []
