from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    pass


class DateTimeMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        nullable=False,
        onupdate=func.now(),
    )
