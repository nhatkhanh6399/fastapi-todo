from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from app.database import get_db
from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        session: AsyncSession = Depends(get_db),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo


CurrentAsyncSession = Annotated[AsyncSession, Depends(get_db)]
