from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class SqlAlchemyBase(AsyncAttrs, DeclarativeBase):
    ...


DATABASE_URL = f"sqlite+aiosqlite://db/database.sqlite"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal: async_sessionmaker = async_sessionmaker(engine)


def create_session() -> async_sessionmaker[AsyncSession]:
    """Return a new database session.

    :return: new database session object.
    """

    global SessionLocal
    return SessionLocal()
