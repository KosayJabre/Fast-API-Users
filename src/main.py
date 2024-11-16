from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from .routers import routers
from .database import engine


app = FastAPI()
for router in routers:
    app.include_router(router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
