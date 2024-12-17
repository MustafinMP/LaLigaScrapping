import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

SqlAlchemyBase = declarative_base()

DATABASE_URL = f"sqlite:///database/laliga.sqlite?check_same_thread=False"
SessionFactory = None


def init_db() -> None:
    global SessionFactory

    if SessionFactory:
        return
    print(os.walk('/'))
    engine = create_engine(DATABASE_URL, echo=False)
    SessionFactory = sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)
    print(f"INFO:     Connected to database")


def create_session() -> Session:
    """Return a new database session.

    :return: new database session object.
    """

    global SessionFactory
    return SessionFactory()
