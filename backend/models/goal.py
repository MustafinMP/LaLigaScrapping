from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_serializer import SerializerMixin

from db_session import SqlAlchemyBase


class Goal(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goal'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    minute: Mapped[int] = mapped_column()

    match_id: Mapped[int] = mapped_column(ForeignKey('match.id'))
    match_ = relationship('Match', foreign_keys=[match_id], backref='goals')

    player_id: Mapped[int] = mapped_column(ForeignKey('player.id'))
    player = relationship('Player', foreign_keys=[player_id], backref='goals')

    assist_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey('player.id'), nullable=True)
    assist_player = relationship('Player', foreign_keys=[assist_player_id], backref='assists')
