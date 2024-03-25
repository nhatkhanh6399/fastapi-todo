from fastapi import APIRouter, Depends, HTTPException, status
from app.deps.api import RoleChecker, get_current_user
from app.deps.db import get_repository
from app.repositories.user import UserRepository
from app.schemas.user import User

router = APIRouter()


@router.get("/{user_id}", response_model=User)
async def read_user(
    user_id: int,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    current_user: User = Depends(get_current_user),
    authorzied=Depends(RoleChecker(["admin"])),
):
    user = await user_repo.read_user(user_id=user_id)
    # stmt = (
    #     select(User)
    #     .join(User.todos)
    #     .options(contains_eager(User.todos))
    #     .where(User.id == user_id)
    #     # .where(Todo.complete == True)
    #     .order_by(Todo.id.desc())
    #     .execution_options(populate_existing=True)
    # )

    # print(stmt)

    # result = await session.execute(stmt)

    # user = result.scalars().first()

    # if user.todos is not None:
    #     user.todos = [todo for todo in user.todos if todo.id > 2]
    # else:
    #     user.todos = []

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
