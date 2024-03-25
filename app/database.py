from typing import Annotated
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.settings import settings
from app.models.common import Base

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app/tasks.db"
# SQLALCHEMY_DATABASE_URL: PostgresDsn = (
#     "postgresql+asyncpg://postgres:123456@127.0.0.1/postgres"
# )

print(str(settings.SQLALCHEMY_DATABASE_URI))

# engine = create_async_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def init_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    await init_connection()
    async with SessionLocal() as session:
        yield session
