from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Team(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'team'

    laliga_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)