from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.deps.api import get_current_user, get_service
from app.deps.db import get_repository
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserRequest, User, UserToken
from fastapi.security import OAuth2PasswordRequestForm

from app.services.auth import AuthService

router = APIRouter()


@router.get("/me", response_model=User)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: CreateUserRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    auth_service: AuthService = Depends(get_service(AuthService)),
):
    return await auth_service.create_user(user=user, user_repo=user_repo)


@router.post("/login", response_model=UserToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    auth_service: AuthService = Depends(get_service(AuthService)),
):
    return await auth_service.login_for_access_token(
        username=form_data.username, password=form_data.password, user_repo=user_repo
    )
