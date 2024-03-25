from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from app.models.common import Base, DateTimeMixin

if TYPE_CHECKING:
    from app.models.user import User


class Task(Base, DateTimeMixin):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[int] = mapped_column(Integer)
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship(back_populates="tasks")
