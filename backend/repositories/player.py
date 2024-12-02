from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions

from models.goal import Goal
from models.player import Player


class PlayerRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, name: int, nickname, team_id: int):
        player = Player()
        player.name = name
        player.nickname = nickname
        player.team_id = team_id
        self.session.add(player)
        self.session.commit()

    def get_by_name_and_team_id(self, name: str, team_id: int) -> Player:
        stmt = select(Player).where(
            and_(
                Player.name == name,
                Player.team_id == team_id
            )
        )
        return self.session.scalar(stmt)

    def get_all(self):
        stmt = select(Player).outerjoin(Player.goals)
        return self.session.scalars(stmt).all()