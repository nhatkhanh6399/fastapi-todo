from datetime import timedelta
from fastapi import Depends, HTTPException, status
from app.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.deps.db import get_repository
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserRequest
from app.services.base import BaseService


class AuthService(BaseService):
    async def create_user(
        self,
        user: CreateUserRequest,
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
    ):
        duplicated_user = await user_repo.get_duplicated_user(user_create=user)

        if duplicated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The username or email already exists",
            )

        # if duplicated_user.email == user.email:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="The email already exists",
        #     )

        return await user_repo.create_user(user=user)

    async def login_for_access_token(
        self,
        username: str,
        password: str,
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
    ):
        user = await user_repo.authenticate_user(username=username, password=password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )

        token = create_access_token(
            payload={"sub": user.username, "role": user.role, "id": user.id},
            expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return {"access_token": token, "token_type": "bearer"}
