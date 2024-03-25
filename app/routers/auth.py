from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.deps.api import get_current_user
from app.deps.db import get_repository
from app.repositories.user import UserRepository
from app.schemas.user import CreateUserRequest, User, UserToken
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.get("/me", response_model=User)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    user: CreateUserRequest,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    return await user_repo.create_user(user=user)


@router.post("/login", response_model=UserToken)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    user = await user_repo.authenticate_user(
        username=form_data.username, password=form_data.password
    )
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
