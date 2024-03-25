from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.deps.api import get_current_user
from app.deps.db import CurrentAsyncSession, get_repository
from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskRequest, TaskOut, UpdateTaskRequest
from app.schemas.user import User

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
async def read_tasks(
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    tasks = await task_repo.read_tasks(current_user=current_user)

    # if not tasks:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Tasks not found"
    #     )

    return tasks


@router.post("/", response_model=TaskOut)
async def create_task(
    task: CreateTaskRequest,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    create_task_model = Task(**task.model_dump(), user_id=current_user.id)
    return await task_repo.create_task(task=create_task_model)


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(
    task_id: int,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    task = await task_repo.get_task_by_id(task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_update: UpdateTaskRequest,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    task = await task_repo.get_task_by_id(task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return await task_repo.update_task(task=task, task_update=task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    task = await task_repo.get_task_by_id(task_id=task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return await task_repo.delete_task(task=task)
