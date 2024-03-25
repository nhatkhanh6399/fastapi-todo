from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest


class TaskRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def read_tasks(self, current_user: User):
        if current_user.role == "user":
            tasks = await self.connection.execute(
                select(Task).where(Task.user_id == current_user.id)
            )
        if current_user.role == "admin":
            tasks = await self.connection.execute(select(Task))

        return tasks.scalars().all()

    async def get_task_by_id(self, *, task_id: int):
        stmt = select(Task).where(Task.id == task_id)
        result = await self.connection.execute(stmt)
        return result.scalars().first()

    async def create_task(self, *, task: Task):
        self.connection.add(task)
        await self.connection.commit()
        await self.connection.refresh(task)
        return task

    async def update_task(self, *, task: Task, task_update: UpdateTaskRequest):
        task_dict = task_update.model_dump(exclude_unset=True)

        for key, value in task_dict.items():
            setattr(task, key, value)

        self.connection.add(task)
        await self.connection.commit()
        await self.connection.refresh(task)
        return task

    async def delete_task(self, *, task: Task):
        await self.connection.delete(task)
        await self.connection.commit()
