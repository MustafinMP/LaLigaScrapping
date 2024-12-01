from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Match(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'match'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, index=True)
    date: Mapped[str] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, index=True)
    home_score: Mapped[int] = mapped_column()
    away_score: Mapped[int] = mapped_column()

    home_team_id: Mapped[int] = mapped_column(ForeignKey('team.laliga_id'))
    home_team = relationship('Team', foreign_keys=[home_team_id])

    away_team_id: Mapped[int] = mapped_column(ForeignKey('team.laliga_id'))
    away_team = relationship('Team', foreign_keys=[away_team_id])