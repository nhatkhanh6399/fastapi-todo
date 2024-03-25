from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import CreateUserRequest


class UserRepository(BaseRepository):
    def __init__(self, conn: AsyncSession) -> None:
        super().__init__(conn)

    async def read_user(self, *, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.connection.execute(stmt)
        return result.scalars().first()

    async def create_user(self, *, user: CreateUserRequest) -> User:
        create_user_model = User(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            password=get_password_hash(user.password),
            role=user.role,
            is_active=True,
        )

        self.connection.add(create_user_model)
        await self.connection.commit()
        await self.connection.refresh(create_user_model)
        return create_user_model

    async def authenticate_user(self, *, username: str, password: str) -> User:
        stmt = select(User).where(User.username == username)
        result = await self.connection.execute(stmt)
        user = result.scalars().first()

        if not user:
            return None
        if not user.get_user_password_validation(password):
            return None

        return user
