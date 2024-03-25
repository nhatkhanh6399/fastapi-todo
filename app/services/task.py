from fastapi import Depends, HTTPException, status
from app.deps.db import get_repository
from app.models.task import Task
from app.models.user import User
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest
from app.services.base import BaseService


class TaskService(BaseService):
    async def read_tasks(
        self,
        current_user: User,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    ):
        return await task_repo.read_tasks(current_user=current_user)

    async def get_task_by_id(
        self,
        task_id: int,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    ) -> Task:
        task = await task_repo.get_task_by_id(task_id=task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        return task

    async def create_task(
        self,
        task: CreateTaskRequest,
        current_user: User,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    ):
        create_task_model = Task(**task.model_dump(), user_id=current_user.id)
        return await task_repo.create_task(task=create_task_model)

    async def update_task(
        self,
        task: Task,
        task_update: UpdateTaskRequest,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    ):
        return await task_repo.update_task(task=task, task_update=task_update)

    async def delete_task(
        self,
        task_id: int,
        current_user: User,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    ):
        task = await task_repo.get_task_by_id(task_id=task_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        if task.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        return await task_repo.delete_task(task=task)
