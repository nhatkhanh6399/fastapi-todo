from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_connection
from app.routers import api_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # await init_connection()


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api")

    return app


app = get_app()
