from fastapi import Depends, HTTPException, status
from app.deps.db import get_repository
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.base import BaseService


class AdminService(BaseService):
    async def read_user(
        self,
        user_id: User,
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
    ):
        user = await user_repo.read_user(user_id=user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user
