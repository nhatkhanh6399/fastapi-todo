from fastapi import APIRouter, Depends, status

from app.deps.api import get_current_user, get_service
from app.deps.db import get_repository
from app.models.task import Task
from app.repositories.task import TaskRepository
from app.schemas.task import CreateTaskRequest, TaskOut, UpdateTaskRequest
from app.schemas.user import User
from app.services.task import TaskService

router = APIRouter()


@router.get("/", response_model=list[TaskOut])
async def read_tasks(
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    task_service: TaskService = Depends(get_service(TaskService)),
    current_user: User = Depends(get_current_user),
):
    tasks = await task_service.read_tasks(
        current_user=current_user, task_repo=task_repo
    )

    return tasks


@router.post("/", response_model=TaskOut)
async def create_task(
    task: CreateTaskRequest,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    task_service: TaskService = Depends(get_service(TaskService)),
    current_user: User = Depends(get_current_user),
):
    return await task_service.create_task(
        task=task, current_user=current_user, task_repo=task_repo
    )


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(
    task_id: int,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    task_service: TaskService = Depends(get_service(TaskService)),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_task_by_id(task_id=task_id, task_repo=task_repo)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: int,
    task_update: UpdateTaskRequest,
    task_service: TaskService = Depends(get_service(TaskService)),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    current_user: User = Depends(get_current_user),
):
    task = await task_service.get_task_by_id(task_id=task_id, task_repo=task_repo)
    return await task_repo.update_task(task=task, task_update=task_update)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
    task_service: TaskService = Depends(get_service(TaskService)),
    current_user: User = Depends(get_current_user),
):
    return await task_service.delete_task(
        task_id=task_id, task_repo=task_repo, current_user=current_user
    )
