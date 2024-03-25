from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.core.security import verify_password
from app.models.common import Base, DateTimeMixin

if TYPE_CHECKING:
    from app.models.task import Task


class User(Base, DateTimeMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String)

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    def get_user_password_validation(self, password) -> bool:
        user_password_checked = verify_password(password, self.password)
        return user_password_checked
