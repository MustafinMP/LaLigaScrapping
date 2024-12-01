from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

SqlAlchemyBase = declarative_base()

DATABASE_URL = f"sqlite:///database/laliga.sqlite?check_same_thread=False"
SessionFactory = None


def init_app() -> None:
    global SessionFactory

    if SessionFactory:
        return
    print(f"Подключение к базе данных")
    engine = create_engine(DATABASE_URL, echo=False)
    SessionFactory = sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    """Return a new database session.

    :return: new database session object.
    """

    global SessionFactory
    return SessionFactory()
