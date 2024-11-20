from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel
from .routers import routers
from .database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


for router in routers:
    app.include_router(router)
