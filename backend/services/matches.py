import db_session
from repositories.match import MatchRepository


class MatchService:
    @staticmethod
    def get_all() -> dict:
        with db_session.create_session() as session:
            repository = MatchRepository(session)
            return list(map(MatchService._match_to_dict, repository.get_all()))

    @staticmethod
    def _match_to_dict(match_):
        match_dict = match_.to_dict(
                    only=[
                        'date',
                        'home_score',
                        'away_score',
                        'home_team.name',
                        'home_team.image',
                        'away_team.name',
                        'away_team.image'
                    ]
                )
        match_dict['date'] = match_dict['date'].split('T')[0]
        return match_dict
