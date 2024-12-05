import db_session
from repositories.match import MatchRepository
from repositories.team import TeamRepository


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

    @staticmethod
    def get_rating_table():
        with db_session.create_session() as session:
            team_repository = TeamRepository(session)
            teams = {
                team.laliga_id: team.to_dict(
                    only=[
                        'name',
                        'image',
                    ]
                ) | {'points': 0, 'match_count': 0, 'wins': 0, 'loses': 0, 'draws': 0}
                for team in team_repository.get_all()
            }
            match_repository = MatchRepository(session)
            for match_ in match_repository.get_all():
                if match_.home_score > match_.away_score:
                    teams[match_.home_team_id]['points'] += 3
                    teams[match_.home_team_id]['wins'] += 1
                    teams[match_.away_team_id]['loses'] += 1
                elif match_.away_score > match_.home_score:
                    teams[match_.away_team_id]['points'] += 3
                    teams[match_.away_team_id]['wins'] += 1
                    teams[match_.home_team_id]['loses'] += 1
                else:
                    teams[match_.home_team_id]['points'] += 1
                    teams[match_.away_team_id]['points'] += 1
                    teams[match_.away_team_id]['draws'] += 1
                    teams[match_.home_team_id]['draws'] += 1
                teams[match_.home_team_id]['match_count'] += 1
                teams[match_.away_team_id]['match_count'] += 1
            return sorted(teams.values(), key=lambda t: t['points'], reverse=True)

