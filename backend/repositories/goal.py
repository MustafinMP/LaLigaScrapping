from sqlalchemy.orm import Session

from models.goal import Goal


class GoalRepository:
    def __init__(self, session: Session) -> None:
        self.session: Session = session

    def add(self, minute: int, match, player, assist_player = None) -> Goal:
        goal = Goal()
        goal.minute = minute
        goal.match_ = match
        goal.player = player
        if assist_player:
            goal.assist_player = assist_player
        self.session.add(goal)
        self.session.commit()