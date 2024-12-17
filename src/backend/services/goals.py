import db_session
from repositories.goal import GoalRepository


class GoalsService:
    @staticmethod
    def get_all() -> dict:
        with db_session.create_session() as session:
            repository = GoalRepository(session)
            return [
                goal.to_dict(only=[
                    'player.name',
                    'assist_player.name',
                    'match_.date'
                ])
                for goal in repository.get_all()
            ]

    @staticmethod
    def get_goal_count():
        with db_session.create_session() as session:
            repository = GoalRepository(session)
            return [
                goal.to_dict(only=[
                    'player.nickname',
                    'count_1',
                    'id'
                ])
                for goal in repository.get_goal_count()
            ]
