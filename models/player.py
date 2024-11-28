from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Player(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'player'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    nickname: Mapped[str] = mapped_column(String)

    team_id: Mapped[int] = mapped_column(ForeignKey('team.id'))
    team = relationship('Team')