from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from models.match import Match
from models.team import Team


class MatchRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(
            self,
            url: str,
            slug: str,
            date: str,
            home_score: int,
            away_score: int,
            home_team: Team,
            away_team: Team
    ) -> None:
        match_object = Match()
        match_object.url = url
        match_object.slug = slug
        match_object.date = date
        match_object.home_score = home_score
        match_object.away_score = away_score
        match_object.home_team = home_team
        match_object.away_team = away_team
        self.session.add(match_object)
        self.session.commit()

    def get_by_url(self, url: str) -> Match:
        stmt = select(Match).where(Match.url == url)
        return self.session.scalar(stmt)

    def get_all(self) -> list[Match]:
        stmt = select(Match).order_by(desc(Match.date))
        return self.session.scalars(stmt).unique().all()

