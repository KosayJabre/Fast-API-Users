from sqlalchemy import create_engine
from sqlmodel import Session


DB_NAME = "database.db"
SQLITE_URL = f"sqlite:///{DB_NAME}"


engine = create_engine(SQLITE_URL)


def get_session():
    with Session(engine) as session:
        yield session
