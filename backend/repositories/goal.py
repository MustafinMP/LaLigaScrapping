from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions

from models.goal import Goal


class GoalRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, minute: int, match, player, assist_player=None) -> Goal:
        goal = Goal()
        goal.minute = minute
        goal.match_ = match
        goal.player = player
        if assist_player:
            goal.assist_player = assist_player
        self.session.add(goal)
        self.session.commit()

    def get_all(self) -> list[Goal]:
        stmt = select(Goal).order_by(Goal.player_id)
        return self.session.scalars(stmt).all()

    def get_goal_count(self):
        stmt = select(Goal.player, functions.count(Goal.player_id)).group_by(Goal.player_id)
        print(stmt)
        return self.session.scalars(stmt).all()