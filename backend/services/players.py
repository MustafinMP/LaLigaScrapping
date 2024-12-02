from sqlalchemy_serializer import serialize_collection

import db_session
from repositories.player import PlayerRepository


class PlayerService:
    @staticmethod
    def get_all() -> dict:
        with db_session.create_session() as session:
            repository = PlayerRepository(session)
            return PlayerService._goal_count_serializer(set(repository.get_all()))

    @staticmethod
    def _goal_count_serializer(players):
        players_dicts = serialize_collection(
            players, only=[
                'nickname',
                'team.name',
                'team.image',
                'goals.id'
            ]
        )
        for player in players_dicts:
            player['goals_count'] = len(player['goals'])
            del player['goals']
        return sorted(players_dicts, key=lambda p: p['goals_count'], reverse=True)
