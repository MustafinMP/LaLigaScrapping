from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from models.team import Team


class TeamRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def get_by_laliga_id(self, laliga_id: int) -> Team:
        stmt = select(Team).where(Team.laliga_id == laliga_id)
        return self.session.scalar(stmt)

    def add(self, name: str, laliga_id: int, image: str) -> None:
        team = self.get_by_laliga_id(laliga_id)
        if team is None:
            team = Team()
            team.name = name
            team.laliga_id = laliga_id
            team.image = image
            self.session.add(team)
            self.session.commit()