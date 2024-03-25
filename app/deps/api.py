from collections.abc import Callable
from typing import Annotated
from fastapi import Depends, HTTPException, status

from app.core.jwt import oauth2_scheme, verify_jwt_token
from app.deps.db import get_repository
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.admin import AdminService
from app.services.base import BaseService


def get_service(service_type: type[BaseService]) -> Callable[[], BaseService]:
    def _get_service() -> BaseService:
        return service_type()

    return _get_service


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    user_service: AdminService = Depends(get_service(AdminService)),
) -> User:
    token_payload = await verify_jwt_token(token)

    user = await user_service.read_user(
        user_id=token_payload["id"], user_repo=user_repo
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user


class RoleChecker:
    def __init__(self, roles):
        self.roles = roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
